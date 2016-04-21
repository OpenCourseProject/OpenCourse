from django.core.management.base import BaseCommand, CommandError
from course.models import Course, CourseVersion, QueryLog
from datetime import datetime
from datetime import time
from django.utils import timezone
import json
import pytz
import operator
import random

class Command(BaseCommand):
    help = 'Creates intial course versions'
    term_value = 201610

    date_min = datetime(year=2015, month=10, day=30)
    date_max = datetime(year=2015, month=11, day=15)
    pytz.timezone(timezone.get_default_timezone_name()).localize(date_min)
    pytz.timezone(timezone.get_default_timezone_name()).localize(date_max)

    def handle(self, *args, **options):
        courses = Course.objects.filter(term__value=self.term_value)
        versions = CourseVersion.objects.filter(
            term__value=self.term_value,
            time_created__gt=self.date_min,
            time_created__lt=self.date_max)
        self.find_seats(courses)
        self.find_types(courses)
        # self.find_subjects(courses)
        # self.compare_subjects(courses, Course.objects.filter(term__value=201600))
        # self.graph_seats_history(versions)
        # self.find_new_courses(courses, datetime.datetime(year=2015, month=8, day=24))
        # self.find_status(courses)
        # self.find_seats(courses.order_by('-seats')[:5])
        # self.graph_seats_time(courses, range(8, 21))
        # self.find_seats(courses.filter(instructor__rmp_score__isnull=False).order_by('-instructor__rmp_score')[:50])
        # self.find_new_courses(courses, datetime.datetime(year=2015, month=8, day=24, hour=5), datetime.datetime(year=2015, month=8, day=24, hour=15))
        #self.find_queries()

    def find_seats(self, courses):
        seats = 0
        max = 0
        max_course = None
        closed = 0
        self.stdout.write('Finding seats for ' + str(len(courses)) + ' courses')
        for course in courses:
            seats = seats + course.seats
            if course.seats == 0:
                closed += 1
            if course.seats > max:
                max = course.seats
                max_course = course
        self.stdout.write('Total: ' + str(seats))
        self.stdout.write('Average: ' + str(float(seats) / len(courses)))
        self.stdout.write('Max: ' + str(max) + ' (' + str(max_course) + ', ' + str(max_course.crn) + ')')
        self.stdout.write('Closed: ' + str(closed))

    def find_queries(self):
        queries = QueryLog.objects.filter(term__value=self.term_value)
        self.stdout.write('Searching ' + str(len(queries)) + ' queries')
        values = {}
        failed = []
        unique = []
        users = {}
        returned = 0
        fields = {}
        subjects = {}
        days = {}
        instructors = {}
        attributes = {}
        times = {}
        subj_total = 0
        instr_total = 0
        attr_total = 0
        for query in queries:
            if query.results == 0:
                failed.append(query.data)
                continue
            returned += query.results
            iden = query.user.email if query.user else 'none'
            users[iden] = users[iden] + 1 if iden in users else 1
            if query.data not in unique:
                unique.append(query.data)
            data = json.loads(query.data)
            if len(data) > 0:
                if len(data) == 1 and 'show_closed' in data:
                    continue
                for key, value in data.iteritems():
                    fields[key] = fields[key] + 1 if key in fields else 1
                    if key == 'course':
                        subj_total += 1
                        subject = value.split(" ")[0].upper()
                        subjects[subject] = subjects[subject] + 1 if subject in subjects else 1
                    if key == 'days':
                        days[value.upper()] = days[value.upper()] + 1 if value.upper() in days else 1
                    if key == 'instructor':
                        instr_total += 1
                        instructors[value.upper()] = instructors[value.upper()] + 1 if value.upper() in instructors else 1
                    if key == 'attribute':
                        attr_total += 1
                        attributes[value.upper()] = attributes[value.upper()] + 1 if value.upper() in attributes else 1
                    if key == 'start':
                        times[value] = times[value] + 1 if value in times else 1

        sorted_users = sorted(users.items(), key=operator.itemgetter(1))
        self.stdout.write('Total results: ' + str(returned))
        self.stdout.write('Unique searches ' + str(len(unique)) + ': ')
        self.stdout.write('Searches with results ' + str(len(queries) - len(failed)))
        #self.stdout.write('Users ' + str(len(users)) + ': ' + str(sorted_users))
        keys = []
        for key, value in fields.iteritems():
            obj = {'label': key, 'value': value}
            keys.append(obj)
        self.stdout.write('Keys: ' + json.dumps(keys))
        sorted_subjects = sorted(subjects.items(), key=operator.itemgetter(1))
        sorted_instructors = sorted(instructors.items(), key=operator.itemgetter(1))
        sorted_attributes = sorted(attributes.items(), key=operator.itemgetter(1))
        new_days = []
        for key, value in days.iteritems():
            obj = {'label': key, 'value': value}
            new_days.append(obj)
        new_times = []
        for key, value in times.iteritems():
            new_key = datetime.strptime(key, '%H:%M:%S').strftime('%I:%M %p')
            obj = {'label': new_key, 'value': value}
            new_times.append(obj)
        self.stdout.write('Subjects: ' + json.dumps(sorted_subjects) + '(' + str(subj_total) + ')')
        self.stdout.write('Days: ' + json.dumps(new_days))
        self.stdout.write('Times: ' + json.dumps(new_times))
        self.stdout.write('Instructors: ' + json.dumps(sorted_instructors) + '(' + str(instr_total) + ')')
        self.stdout.write('Attrs: ' + json.dumps(sorted_attributes) + '(' + str(attr_total) + ')')

    def find_types(self, courses):
        types = courses.order_by().values_list('ctype', flat=True).distinct()
        self.stdout.write('Finding courses for ' + str(len(types)) + ' types')
        values = []
        for t in types:
            courses = Course.objects.filter(term__value=self.term_value).filter(ctype=t)
            obj = {'label': t, 'value': len(courses)}
            values.append(obj)
        self.stdout.write(json.dumps(values))

    def find_subjects(self, courses):
        self.stdout.write('Finding subjects for ' + str(len(courses)) + ' courses')
        values = {}
        for course in courses:
            subject = course.course.split(' ')[0]
            values[subject] = values[subject] + 1 if subject in values else 1
        subjects = []
        for key, value in values.iteritems():
            obj = {'label': key, 'value': value}
            subjects.append(obj)
        self.stdout.write(json.dumps(subjects))
        return values

    def compare_subjects(self, courses1, courses2):
        values1 = self.find_subjects(courses1)
        values2 = self.find_subjects(courses2)
        missing1 = []
        missing2 = []
        diff = {}
        for key, value in values1.iteritems():
            if not key in values2:
                missing2.append(key)
            else:
                diff[key] = values1[key] - values2[key]
        for key, value in values2.iteritems():
            if not key in values1:
                missing1.append(key)
            else:
                diff[key] = values1[key] - values2[key]
        self.stdout.write('Missing in the first set: ' + json.dumps(missing1))
        self.stdout.write('Missing in the second set: ' + json.dumps(missing2))
        self.stdout.write('Diff: ' + json.dumps(diff))

    def graph_seats_time(self, courses, range):
        seats = []
        self.stdout.write('Creating graphs for ' + str(len(list(range))) + ' hours')
        for i in range:
            value = time(hour=i)
            values = courses.filter(meeting_times__start_time=value)
            if (len(values) > 0):
                avg = 0
                for course in values:
                    avg += course.seats
                avg = float(avg) / len(values)
                obj = {'label': value.strftime('%I %p'), 'value': '{0:.3g}'.format(avg)}
                seats.append(obj)
        self.stdout.write(json.dumps(seats))

    def graph_seats_history(self, courses):
        times = courses.datetimes('time_created', 'hour')
        seats = []
        self.stdout.write('Creating graphs for ' + str(len(times)) + ' versions')
        i = 0
        for time in times:
            i += 1
            self.stdout.write('-> Calculating seats for: ' + str(time))
            versions = CourseVersion.objects.filter(
                time_created__year=time.year,
                time_created__month=time.month,
                time_created__day=time.day,
                time_created__hour=time.hour)
            total = 0
            excluded_values = set([])
            for version in versions:
                value = version.field_list()['seats']
                total += value
                excluded_values.add(version.get_course().id)
            others = Course.objects.exclude(id__in=excluded_values)
            for other in others:
                latest = self.get_last_version(other, time)
                if latest:
                    value = latest.field_list()['seats']
                    total += value
            obj = {'x': str(int(time.strftime("%s")) * 1000), 'y': total}
            seats.append(obj)
            self.stdout.write('-> Seats: ' + str(total))
        self.stdout.write(json.dumps(seats))

    def find_status(self, courses):
        closed_list = []
        open_list = []
        self.stdout.write('Calculating statuses for ' + str(len(courses)) + ' courses')
        for course in courses:
            versions = CourseVersion.objects.find(course)
            closed = True
            open = True
            for version in versions:
                status = version.field_list()['status']
                if status == Course.CLOSED:
                    open = False
                if status == Course.OPEN:
                    closed = False
            if open:
                open_list.append(course)
            if closed:
                closed_list.append(course)
        self.stdout.write('-> Always closed: ' + str(len(closed_list)))
        self.find_subjects(closed_list)
        self.stdout.write('-> Always open: ' + str(len(open_list)))
        self.find_subjects(open_list)


    def find_new_courses(self, courses, after, before=None):
        after = pytz.utc.localize(after)
        if before:
            before = pytz.utc.localize(before)
        self.stdout.write('Finding courses added after ' + str(after) + ', before ' + str(before))
        new = []
        for course in courses:
            earliest = CourseVersion.objects.find(course).earliest('time_created')
            if earliest.time_created >= after:
                if before:
                    if earliest.time_created <= before:
                        new.append(course.id)
                else:
                    new.append(course.id)
        self.stdout.write('-> New courses: ' + str(len(new)))
        self.stdout.write(json.dumps(list(new)))
        self.find_types(Course.objects.filter(id__in=new))
        self.find_subjects(Course.objects.filter(id__in=new))

    def get_last_version(self, course, time):
        versions = CourseVersion.objects.filter(term=course.term, course_crn=course.crn, time_created__lt=time)
        if len(versions):
            return versions.latest('time_created')
        else:
            return None
