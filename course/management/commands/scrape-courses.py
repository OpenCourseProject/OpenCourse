from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from course.models import Course, Term, Instructor, FollowEntry
from splinter import Browser
from lxml import html
import json
import datetime

class Command(BaseCommand):
    help = 'Scrapes the CNU courses'

    def handle(self, *args, **options):
    	# Visit URL
    	url = "https://pulsar.cnu.edu/soc/socquery.aspx"
    	browser = Browser('phantomjs')
    	browser.visit(url)
        # Parse page HTML
        page = html.fromstring(browser.html)
        # Get semester select options
        semesterlist = page.xpath(".//select[@name='semesterlist']/option")
        # Get rid of all the existing entries
        if len(semesterlist) > 0:
            Term.objects.all().delete()
        # Add all the new entries
        for entry in semesterlist:
            # Term ID
            value = int(entry.attrib['value'])
            # Term Name
            name = entry.text.strip()
            # Save it to the database
            term = Term(value=value, name=name)
            term.save()

            # Visit the query page
            browser.visit(url)
            # Select the relevant term
            browser.select('startyearlist', '2')
            browser.select('semesterlist', str(value))
            # Find and click the 'search' button
            button = browser.find_by_id('Button1').click()

            # Parse new HTML
            page = html.fromstring(browser.html)
        	# Get rows from the table
            rows = page.get_element_by_id('GridView1').xpath('tbody')[0]
            courses = []
            skip = True
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
                days = row.getchildren()[7].text.strip()

                start_time = None
                end_time = None
                timestring = row.getchildren()[8].text.strip()

                # Not all classes have a time set
                if len(timestring) > 0:
                    start_time = timestring.split('-')[0]
                    if len(start_time) == 3:
                        start_time = '0' + start_time
                    end_time = timestring.split('-')[1]
                    if len(end_time) == 3:
                        end_time = '0' + end_time
                    start_time = datetime.datetime.strptime(start_time, '%H%M').time()
                    end_time = datetime.datetime.strptime(end_time, '%H%M').time()

                location = row.getchildren()[9].text.strip()
                instructor = row.getchildren()[10].text.strip()

                # Parse the instructor
                if instructor and len(instructor) > 0:
                    arr = instructor.split(", ")
                    last_name = arr[0]
                    first_name = None
                    if len(arr) > 1:
                        first_name = arr[1]

                # Create the instructor
                instructor = Instructor(first_name=first_name, last_name=last_name)

                # Add it to the database
                try:
                    obj = Instructor.objects.get(first_name=first_name, last_name=last_name)
                    opts = obj._meta
                    for f in opts.fields:
                        if f.name != 'id':
                            setattr(obj, f.name, getattr(instructor, f.name))
                        obj.save()
                    instructor = obj
                except Instructor.DoesNotExist:
                    instructor.save()

                seats = int(row.getchildren()[11].xpath('span')[0].text.strip())
                statusstring = row.getchildren()[12].xpath('span')[0].text.strip()
                status = 1 if statusstring == 'Open' else 0 if statusstring == 'Closed' else -1

                # Create the course
                course = Course(term=term, crn=crn, course=course, course_link=course_link, section=section, title=title, bookstore_link=bookstore_link, hours=hours, attributes=attributes, ctype=ctype, days=days, start_time=start_time, end_time=end_time, location=location, instructor=instructor, seats=seats, status=status)

                # Add it to the database
                try:
                    obj = Course.objects.get(term=term, crn=crn)
                    opts = obj._meta
                    status_update = False
                    for f in opts.fields:
                        if f.name != 'id':
                            old_attr = getattr(obj, f.name)
                            new_attr = getattr(course, f.name)
                            setattr(obj, f.name, new_attr)
                            if f.name == 'status':
                                if old_attr != new_attr:
                                    status_update = True
                    obj.save()
                    if status_update:
                        follows = FollowEntry.objects.filter(course=obj)
                        for follow in follows:
                            call_command('email', str(follow.user.id), str(obj.term.value), str(obj.crn))
                except Course.DoesNotExist:
                    course.save()
        self.stdout.write('Successfully scraped courses')
