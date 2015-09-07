from django.core.management.base import BaseCommand, CommandError
from course.models import Course, CourseVersion
import json
import datetime
import pytz

class Command(BaseCommand):
    help = 'Creates intial course versions'
    term_value = 201600

    def handle(self, *args, **options):
        courses = Course.objects.filter(term__value=self.term_value)
        # self.find_seats(courses)
        # self.find_types(courses)
        # self.find_subjects(courses)
        # self.graph_seats_history(courses)
        # self.find_new_courses(courses, datetime.datetime(year=2015, month=8, day=24))
        # self.find_status(courses)
        # self.find_seats(courses.order_by('-seats')[:5])
        # self.graph_seats_time(courses, range(8, 21))
        # self.find_seats(courses.filter(instructor__rmp_score__isnull=False).order_by('-instructor__rmp_score')[:50])
        self.find_new_courses(courses, datetime.datetime(year=2015, month=8, day=24, hour=5), datetime.datetime(year=2015, month=8, day=24, hour=15))

    def find_seats(self, courses):
        seats = 0
        max = 0
        max_course = None
        closed = 0
        self.stdout.write('Finding seats for ' + str(len(courses)) + ' courses')
        for course in courses:
            print 'http://opencourseproject.com/course/' + str(course.term.value) + '/' + str(course.crn) + '/'
            seats = seats + course.seats
            if course.seats == 0:
                closed += 1
            if course.seats > max:
                max = course.seats
                max_course = course
        self.stdout.write('Total: ' + str(seats))
        self.stdout.write('Average: ' + str(float(seats) / len(courses)))
        self.stdout.write('Max: ' + str(max) + ' (' + str(course) + ', ' + str(course.crn) + ')')
        self.stdout.write('Closed: ' + str(closed))

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
            subject = course.course
            values[subject] = values[subject] + 1 if subject in values else 1
        subjects = []
        for key, value in values.iteritems():
            obj = {'label': key, 'value': value}
            subjects.append(obj)
        self.stdout.write(json.dumps(subjects))

    def graph_seats_time(self, courses, range):
        seats = []
        self.stdout.write('Creating graphs for ' + str(len(list(range))) + ' hours')
        for i in range:
            time = datetime.time(hour=i)
            values = courses.filter(meeting_times__start_time=time)
            if (len(values) > 0):
                avg = 0
                for course in values:
                    avg += course.seats
                avg = float(avg) / len(values)
                obj = {'label': time.strftime('%I %p'), 'value': '{0:.3g}'.format(avg)}
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
            versions = CourseVersion.objects.filter(time_created__year=time.year, time_created__month=time.month, time_created__day=time.day, time_created__hour=time.hour)
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
