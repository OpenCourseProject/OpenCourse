from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from course.models import Course, Term, Instructor, FollowEntry, MeetingTime
from opencourse.models import CourseUpdateLog
from pyvirtualdisplay import Display
from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError
from lxml import html
import json
import datetime
import reversion
from time import sleep

class Command(BaseCommand):
    help = 'Scrapes the CNU courses'

    total_parsed = 0
    total_added = 0
    total_updated = 0

    def handle(self, *args, **options):
        # If present, will allow debugging of scrape without visiting webpage
        test_data = None
        if test_data:
            content = open(test_data).read()
            term = Term.objects.all()[0]
            self.parse_courses(term, html.fromstring(content))
            return
        # Visit URL
    	url = "https://pulsar.cnu.edu/soc/socquery.aspx"
        display = Display(visible=0, size=(1024, 768))
        display.start()
    	browser = Browser('firefox')
        try:
            browser.visit(url)
        except HttpResponseError, e:
            print "Request failed with status code %s: %s" % (e.status_code, e.reason)
        # Parse page HTML
        page = html.fromstring(browser.html)
        # Get semester select options
        semesterlist = page.xpath(".//select[@name='semesterlist']/option")

        # Add all the new entries
        for entry in semesterlist:
            # Term ID
            value = int(entry.attrib['value'])
            # Term Name
            name = entry.text.strip()
            # Save it to the database
            term = Term(value=value, name=name)
            try:
                term = Term.objects.get(value=value)
            except Term.DoesNotExist:
                term.save()

            self.stdout.write('Parsing classes for: ' + term.name)

            self.stdout.write('-> Sleeping for 30s...')
            sleep(30)
            self.stdout.write('-> Starting the scrape')
            # Visit the query page
            browser.visit(url)
            # Select the relevant term
            browser.select('startyearlist', '2')
            browser.select('semesterlist', str(value))
            # Find and click the 'search' button
            button = browser.find_by_id('Button1').click()

            # Parse new HTML
            page = html.fromstring(browser.html)
            self.parse_courses(term, page)

        browser.quit()
        display.stop()
        # Create a log
        CourseUpdateLog(courses_parsed=self.total_parsed, courses_added=self.total_added, courses_updated=self.total_updated).save()
        self.stdout.write('Successfully scraped courses')

    def parse_instructor(self, content):
        # Parse the instructor
        arr = content.split(", ")
        last_name = arr[0]
        first_name = None
        if len(arr) > 1:
            first_name = arr[1]

        instructor = Instructor(first_name=first_name, last_name=last_name)
        # Add it to the database
        try:
            if first_name is None:
                instructor = Instructor.objects.get(first_name=first_name, last_name=last_name)
            else:
                instructor = Instructor.objects.get(first_name__startswith=first_name, last_name=last_name)
        except Instructor.DoesNotExist:
            instructor.save()
        except Instructor.MultipleObjectsReturned:
            return None
        return instructor

    def parse_courses(self, term, page):
    	# Get rows from the table
        rows = page.get_element_by_id('GridView1').xpath('tbody')[0]
        skip = True
        added = 0
        updated = 0
        # Parse all rows
        for row in rows:
            # Skip the first row (titles)
            if skip is True:
                skip = False
                continue

            # Parse elements
            crn = int(row.getchildren()[0].text.strip())
            course = row.getchildren()[1].xpath('a')[0].text.strip()
            course_link = row.getchildren()[1].xpath('a')[0].attrib['href']
            section = row.getchildren()[2].text.strip()
            title = row.getchildren()[3].xpath('a')[0].text.strip()
            bookstore_link = row.getchildren()[3].xpath('a')[0].attrib['href']
            hours = row.getchildren()[4].text.strip()
            attrstring = row.getchildren()[5].xpath('span')[0].text
            attributes = attrstring.strip() if attrstring else ''
            ctype = row.getchildren()[6].text.strip()
            meeting_times = []

            # Possibility of having multiple meeting times
            days_list = list(row.getchildren()[7].itertext())
            times_list = list(row.getchildren()[8].itertext())
            for i, days in enumerate(days_list):
                days = days.strip()
                # These don't have a meeting time at all
                if len(days) == 0:
                    continue
                time = MeetingTime(days=days)
                # Not all meeting times have a specific start/end time
                if len(times_list) >= i:
                    timestring = times_list[i].strip()
                    if len(timestring) > 0:
                        start_time = timestring.split('-')[0]
                        if len(start_time) == 3:
                            start_time = '0' + start_time
                        end_time = timestring.split('-')[1]
                        if len(end_time) == 3:
                            end_time = '0' + end_time
                        start_time = datetime.datetime.strptime(start_time, '%H%M').time()
                        end_time = datetime.datetime.strptime(end_time, '%H%M').time()
                        time.start_time = start_time
                        time.end_time = end_time
                        # Add it to the database
                        try:
                            obj = MeetingTime.objects.get(days=days, start_time=time.start_time, end_time=time.end_time)
                            time = obj
                        except MeetingTime.DoesNotExist:
                            time.save()
                        # We store a list of PKs to cut down on queries
                        meeting_times.append(time.id)

            location = row.getchildren()[9].text.strip()
            if location == 'ARR':
                location = None

            instructor = row.getchildren()[10].text.strip()

            # Parse the instructor
            if instructor and len(instructor) > 0:
                instructor = self.parse_instructor(instructor)
            else:
                instructor = None

            seats = int(row.getchildren()[11].xpath('span')[0].text.strip())
            statusstring = row.getchildren()[12].xpath('span')[0].text.strip()
            status = 1 if statusstring == 'Open' else 0 if statusstring == 'Closed' else -1

            # Create the course
            course = Course(term=term, crn=crn, course=course, course_link=course_link, section=section, title=title, bookstore_link=bookstore_link, hours=hours, attributes=attributes, ctype=ctype, location=location, instructor=instructor, seats=seats, status=status)

            # Add it to the database
            try:
                obj = Course.objects.get(term=term, crn=crn)
                if not course.instructor:
                    course.instructor = obj.instructor
                opts = obj._meta
                status_update = False
                for f in opts.fields:
                    if f.name != 'id':
                        old_attr = getattr(obj, f.name)
                        new_attr = getattr(course, f.name)
                        if old_attr != new_attr:
                            updated += 1
                        setattr(obj, f.name, new_attr)
                        if f.name == 'status':
                            if old_attr != new_attr:
                                status_update = True
                obj.meeting_times = meeting_times
                with transaction.atomic(), reversion.create_revision():
                    obj.save()
            except Course.DoesNotExist:
                course.save()
                course.meeting_times = meeting_times
                added += 1

        self.stdout.write('-> Parsed ' + str(len(rows) - 1) + ' courses. ' + str(added) + ' added, ' + str(updated) + ' updated.')
        self.total_parsed += len(rows) - 1
        self.total_added += added
        self.total_updated += updated
