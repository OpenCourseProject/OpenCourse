from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from course.models import Course, Term, Instructor, FollowEntry, MeetingTime
from opencourse.models import TermUpdate, UpdateLog
from pyvirtualdisplay import Display
from splinter import Browser
from splinter.request_handler.status_code import HttpResponseError
from selenium.common.exceptions import TimeoutException
from lxml import html
from datetime import datetime
from django.utils import timezone
from time import sleep
import json
import logging
import kronos
from django.conf import settings
from threading import Timer
import signal
import sys
import traceback
import re
import base64
logger = logging.getLogger('opencourse')

SOC_URL = "https://navigator.cnu.edu/StudentScheduleofClasses/"

@kronos.register(settings.COURSE_UPDATE_INTERVAL)
class Command(BaseCommand):
    help = 'Scrapes the CNU courses'

    def signal_handler(signal, frame):
        self.log('Update process manually aborted')
        self.complete_update(UpdateLog.FAILED)
        sys.exit(0)

    def log(self, text):
        self.stdout.write(text)
        if not self.debug:
            self.update_log.log(text)

    def begin_update(self):
        if not self.debug:
            self.update_log = UpdateLog()
            self.update_log.save()
        self.log('Update started')

    def begin_term(self, term):
        self.term_update = TermUpdate(term=term)
        self.log('Parsing classes for: {}'.format(term.name))
        if not self.debug:
            self.term_update.save()
            self.update_log.updates.add(self.term_update)
            self.update_log.save()

    def complete_term(self, parsed, added, updated, deleted):
        self.log('Parsed {} courses. {} added, {} updated, {} removed.'.format(parsed, added, updated, deleted))
        if not self.debug:
            self.term_update.courses_parsed = parsed
            self.term_update.courses_added = added
            self.term_update.courses_updated = updated
            self.term_update.courses_deleted = deleted
            self.term_update.time_completed = timezone.now()
            self.term_update.save()

    def complete_update(self, status=UpdateLog.SUCCESS):
        if self.browser:
            self.browser.quit()
        if self.display:
            self.display.stop()
        if not self.debug:
            self.update_log.status = status
            self.update_log.time_completed = timezone.now()
            self.update_log.save()
            diff = self.update_log.time_completed - self.update_log.time_created
            minutes, seconds = divmod(diff.seconds, 60)
            status_name = dict(UpdateLog._meta.get_field('status').choices)[status]
            self.log('Update {} in {}m, {}s (status = {})'.format(status_name, minutes, seconds, status))

    def handle(self, *args, **options):
        # If present, will do a dry-run without commiting results to the database
        self.debug = False
        if self.debug:
            self.log('==================DRY RUN==================')
            self.log('Database will be unaffected by any changes')
        # If present, will allow debugging of scrape without visiting webpage
        test_data = None
        if test_data:
            content = open(test_data).read()
            term = Term.objects.all()[0]
            self.parse_courses(term, html.fromstring(content))
            return
        # Begin update process
        self.begin_update()
        self.F_TERM = base64.b64decode('RmFjdWx0eQ==')
        signal.signal(signal.SIGINT, self.signal_handler)
        try:
            self.scrape()
        except Exception as e:
            self.log('ERROR: ' + str(e))
            self.complete_update(UpdateLog.FAILED)
            traceback.print_exc()

    def scrape(self):
        # Visit URL
        self.log('Requesting course information...')
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.browser = Browser('firefox')
        self.browser.driver.set_page_load_timeout(60)
        try:
            self.browser.visit(SOC_URL)
        except HttpResponseError, e:
            self.log('Request failed with status code {}'.format(e.status_code))
            self.complete_update(UpdateLog.FAILED)
            return
        except TimeoutException:
            self.log('Request timed out.')
            self.complete_update(UpdateLog.FAILED)
            return
        # Parse page HTML
        page = html.fromstring(self.browser.html)
        # Get semester select options
        semesterlist = page.xpath(".//select[@name='semesterlist']/option")
        self.log('Received data. Found {} semesters.'.format(len(semesterlist)))

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
                if not self.debug:
                    term.save()
                self.log('Added a new term, {} ({})'.format(name, value))

            if not term.update:
                self.log('Not parsing {} as it has been marked as archived.'.format(term.name))
                continue

            self.begin_term(term)

            total_courses = 0
            added_courses = 0
            updated_courses = 0
            deleted_courses = 0

            vals = [(SOC_URL, False,), (re.sub('S.*t', self.F_TERM, SOC_URL), True,)]
            #vals = [(re.sub('S.*t', self.F_TERM, SOC_URL), True,)]
            for url_val, f_val in vals:
                self.log('Sleeping for 30s...')
                sleep(30)
                self.log('Beginning web scrape')
                # Visit the query page
                try:
                    self.browser.visit(url_val)
                except TimeoutException:
                    self.log('Request timed out.')
                    self.complete_update(UpdateLog.FAILED)
                    return
                # Select the relevant term
                self.browser.select('startyearlist', '2')
                self.browser.select('semesterlist', str(value))
                # Find and click the 'search' button
                button = self.browser.find_by_id('Button1').click()

                # Parse new HTML
                page = html.fromstring(self.browser.html)
                stats = self.parse_courses(term, page, f_val)
                # Log stats
                total_courses = total_courses + stats['total']
                added_courses = added_courses + stats['added']
                updated_courses = updated_courses + stats['updated']
                deleted_courses = deleted_courses + stats['deleted']

            self.complete_term(total_courses, added_courses, updated_courses, deleted_courses)

        # Complete update process
        self.complete_update()

    def parse_instructor(self, content):
        # Parse the instructor
        arr = content.split(", ")
        last_name = arr[0]
        first_name = None
        if len(arr) > 1:
            first_name = arr[1].split(" ")[0]

        instructor = Instructor(first_name=first_name, last_name=last_name)
        # Add it to the database
        try:
            if first_name is None:
                instructor = Instructor.objects.get(first_name=first_name, last_name=last_name)
            else:
                instructor = Instructor.objects.get(first_name__startswith=first_name, last_name=last_name)
        except Instructor.DoesNotExist:
            if not self.debug:
                instructor.save()
            self.log('Added a new instructor: {}'.format(instructor))
        except Instructor.MultipleObjectsReturned:
            return None
        return instructor

    def parse_course(self, term, row, f_mark):
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
                    start_time = datetime.strptime(start_time, '%H%M').time()
                    end_time = datetime.strptime(end_time, '%H%M').time()
                    time.start_time = start_time
                    time.end_time = end_time
                    # Add it to the database
                    try:
                        obj = MeetingTime.objects.get(days=days, start_time=time.start_time, end_time=time.end_time)
                        time = obj
                    except MeetingTime.DoesNotExist:
                        if not self.debug:
                            time.save()
                    meeting_times.append(time)

        location = row.getchildren()[9].text.strip()
        if location == 'ARR':
            location = None

        instructor = row.getchildren()[10].text.strip()

        # Parse the instructor
        if instructor and len(instructor) > 0:
            instructor = self.parse_instructor(instructor)
        else:
            instructor = None

        if f_mark:
            seats = int(row.getchildren()[11].text.strip())
            if seats < 0:
                seats = 0
        else:
            seats = int(row.getchildren()[11].xpath('span')[0].text.strip())
        statusstring = row.getchildren()[12].xpath('span')[0].text.strip()
        status = 1 if statusstring == 'Open' else 0 if statusstring == 'Closed' else -1

        course = Course(term=term, crn=crn, course=course, course_link=course_link, section=section, title=title, bookstore_link=bookstore_link, hours=hours, attributes=attributes, ctype=ctype, location=location, instructor=instructor, seats=seats, status=status, hidden=f_mark)
        return {'course': course, 'meeting_times': meeting_times}

    def parse_courses(self, term, page, f_mark):
        page.make_links_absolute(SOC_URL)
    	# Get rows from the table
        try:
            grid = page.get_element_by_id('GridView1')
            rows = grid.xpath('tbody')[0]
        except:
            rows = []
        crns = []
        skip = True
        added = 0
        updated = 0
        deleted = 0
        # Parse all rows
        for row in rows:
            # Skip the first row (titles)
            if skip is True:
                skip = False
                continue

            # Create the course
            course_values = self.parse_course(term, row, f_mark)
            course = course_values['course']
            meeting_times = course_values['meeting_times']

            # Log the CRN as found
            crns.append(course.crn)

            # Add it to the database
            try:
                obj = Course.objects.get(term=course.term, crn=course.crn)
                if f_mark and not obj.hidden:
                    continue
                if not course.instructor:
                    course.instructor = obj.instructor
                opts = obj._meta
                changed = False
                for f in opts.fields:
                    if f.name not in ['id', 'meeting_times']:
                        old_attr = getattr(obj, f.name)
                        new_attr = getattr(course, f.name)
                        if old_attr != new_attr:
                            logger.debug('Changed value ' + f.name + ': ' + str(old_attr) + ' -> ' + str(new_attr))
                            changed = True
                            setattr(obj, f.name, new_attr)
                if obj.deleted:
                    obj.deleted = False
                    changed = True
                if len([item for item in obj.meeting_times.all() if item not in meeting_times]) > 0:
                    logger.debug('Changed meeting times ' + str(obj.meeting_times.all()) + ' -> ' + str(meeting_times))
                    changed = True
                    obj.meeting_times = course.meeting_times
                if changed:
                    logger.debug('Course listed as changed: /' + str(obj.term.value) + '/' + str(obj.crn))
                    self.log('Updated an existing course, CRN {}'.format(obj.crn))
                    updated += 1
                    if not self.debug:
                        obj.save()
            except Course.DoesNotExist:
                if not self.debug:
                    course.save()
                    course.meeting_times = meeting_times
                self.log('Added a new course, CRN {}'.format(course.crn))
                added += 1
        # Remove courses that didn't show up
        missing_courses = Course.objects.filter(term=term, deleted=False).exclude(crn__in=crns)
        for missing_course in missing_courses:
            missing_course.deleted = True
            if not self.debug:
                missing_course.save()
            self.log('Removed a course that no longer exists, CRN {}'.format(missing_course.crn))
            deleted += 1

        count = 0 if len(rows) is 0 else len(rows) - 1
        stats = {
            'total': count,
            'added': added,
            'updated': updated,
            'deleted': deleted,
        }
        return stats
