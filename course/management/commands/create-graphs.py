from django.core.management.base import BaseCommand, CommandError
from course.models import Term, Course, CourseVersion, QueryLog
from schedule.models import ScheduleEntry
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import pytz
import pygal

@kronos.register(settings.GRAPH_UPDATE_INTERVAL)
class Command(BaseCommand):
    help = 'Generate course graphs'

    def handle(self, *args, **options):
        term = Term.objects.filter(value=201600)
        date_max = datetime.now()
        pytz.timezone(timezone.get_default_timezone_name()).localize(date_max)
        date_list = [date_max - timedelta(hours=x) for x in range(24, 0, -1)]

        courses = Course.objects.filter(term=term)

        self.graph_seats_history(date_list, courses)
        self.graph_schedule_history(date_list, term)

    def graph_seats_history(self, date_list, courses):
        self.stdout.write('Generating seat history graph')
        seats = []
        for date in date_list:
            total = 0
            for course in courses:
                versions = CourseVersion.objects.filter(term=course.term, course_crn=course.crn, time_created__lte=date)
                if len(versions) > 0:
                    version = versions.latest('time_created')
                    total += version.field_list()['seats']
            seats.append(total)
            percent = (len(seats) * 100 / len(date_list))
            self.stdout.write('%s\r' % ('Progress: ' + str(percent) + '%'))
            self.stdout.flush()
        self.render_graph('Open seats in all courses', 'seats_history.svg', date_list, {'Open seats': seats})

    def graph_schedule_history(self, date_list, term):
        self.stdout.write('Generating schedule history graph')
        values = []
        for date in date_list:
            total = 0
            schedules = ScheduleEntry.objects.filter(term=term, time_created__lte=date)
            values.append(len(schedules))
            percent = (len(values) * 100 / len(date_list))
            self.stdout.write('%s\r' % ('Progress: ' + str(percent) + '%'))
            self.stdout.flush()
        self.render_graph('Number of scheduled courses', 'schedule_history.svg', date_list, {'Scheduled courses': values})

    def render_graph(self, title, filename, date_list, values):
        config = pygal.Config()
        config.width=900
        config.height=350
        config.legend_at_bottom=True
        config.fill = True
        config.style = pygal.style.BlueStyle
        config.interpolate = 'cubic'
        config.x_labels_major_every = 4
        config.x_label_rotation = 60

        chart = pygal.Line(config)
        chart.title = title
        chart.x_labels = map(lambda d: d.strftime('%-I:%M %p'), date_list)
        for key, value in values.iteritems():
            chart.add(key, value)
        chart.render_to_file(settings.STATIC_ROOT + '/graphs/' + filename)
