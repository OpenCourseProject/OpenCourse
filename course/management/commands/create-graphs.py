from django.core.management.base import BaseCommand, CommandError
from course.models import Term, Course, CourseVersion, QueryLog, FollowEntry
from schedule.models import ScheduleEntry
from opencourse.models import UpdateLog
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import pytz
import pygal
import kronos
import sys

@kronos.register(settings.GRAPH_UPDATE_INTERVAL)
class Command(BaseCommand):
    help = 'Generate course graphs'

    def handle(self, *args, **options):
        term = Term.objects.get(value=settings.CURRENT_TERM)
        date_max = datetime.now()
        pytz.timezone(timezone.get_default_timezone_name()).localize(date_max)
        date_list = [date_max - timedelta(hours=x) for x in range(24, 0, -1)]

        courses = Course.objects.filter(term=term)
        updates = UpdateLog.objects.all().order_by('-time_created')[:10][::-1] # reversed

        self.graph_query_history(date_list)
        #self.graph_seats_history(date_list, courses, term)
        self.graph_update_changes(updates)

    def graph_seats_history(self, date_list, courses, term):
        self.stdout.write('Generating seat history graph')
        values = []
        #self.print_progress(len(values), len(date_list))
        for date in date_list:
            self.stdout.write(str(date))
            total = 0
            i = 0
            for course in courses:
                self.stdout.write('{}/{}'.format(i, len(courses)))
                versions = CourseVersion.objects.filter(term=course.term, course_crn=course.crn, time_created__lte=date)
                if len(versions) > 0:
                    version = versions.latest('time_created')
                    total += version.fielgraph_update_changesd_list()['seats']
                #self.print_progress(len(values) * (i / len(courses)), len(date_list))
                i += 1
            values.append(total)
        print values
        self.render_graph('Open seats in {} courses'.format(term.name), 'seats_history.svg', date_list, {'Open seats': values})

    def graph_schedule_history(self, date_list):
        self.stdout.write('Generating schedule history graph')
        schedule_values = []
        self.print_progress(len(schedule_values), len(date_list))
        for date in date_list:
            total = 0
            schedules = ScheduleEntry.objects.filter(time_created__lte=date)
            schedule_values.append(len(schedules))
            self.print_progress(len(schedule_values), len(date_list))
        self.stdout.write('Generating follow history graph')
        follow_values = []
        self.print_progress(len(follow_values), len(date_list))
        for date in date_list:
            total = 0
            follows = FollowEntry.objects.filter(time_created__lte=date)
            follow_values.append(len(follows))
            self.print_progress(len(follow_values), len(date_list))

        self.render_graph('Scheduling in the last 24 hours', 'schedule_history.svg', date_list, {
            'Scheduled courses': schedule_values,
            'Followed courses': follow_values
        })

    def graph_query_history(self, date_list):
        self.stdout.write('Generating query history graph')
        query_values = []
        self.print_progress(len(query_values), len(date_list))
        for date in date_list:
            total = 0
            queries = QueryLog.objects.filter(time_created__lte=date, time_created__gte=date - timedelta(hours=1))
            query_values.append(len(queries))
            self.print_progress(len(query_values), len(date_list))
        self.render_graph('Course searches in the last 24 hours', 'query_history.svg', date_list, {'Course searches': query_values}, chart_type=pygal.Bar)

    def graph_update_changes(self, logs):
        self.stdout.write('Generating update history graph')
        updated = []
        added = []
        times = []
        self.print_progress(len(times), len(logs))
        for log in logs:
            time = log.time_created.astimezone(pytz.timezone(timezone.get_default_timezone_name()))
            times.append(time)
            updated.append(log.courses_updated)
            added.append(log.courses_added)
            self.print_progress(len(times), len(logs))
        self.render_graph('Recent course updates', 'course_updates.svg', times, {'Courses Added': added, 'Courses Updated': updated})

    def graph_course_subject(self, courses):
        self.stdout.write('Generating course type graph')
        values = {}
        i = 0
        self.print_progress(i, len(courses))
        for course in courses:
            i += 1
            subject = course.course.split(' ')[0]
            values[subject] = values[subject] + 1 if subject in values else 1
            self.print_progress(i, len(courses))
        self.render_graph('Course subjects', 'course_subjects.svg', None, values, chart_type=pygal.Pie, style=pygal.style.DefaultStyle, show_legend=False)

    def render_graph(self, title, filename, date_list, values, chart_type=pygal.Line, style=pygal.style.BlueStyle, show_legend=True):
        config = pygal.Config()
        config.width=900
        config.height=350
        config.fill = True
        config.style = style

        config.show_legend = show_legend
        if show_legend:
            config.legend_at_bottom=True

        if date_list:
            config.x_labels = map(lambda d: d.strftime('%-I:00 %p'), date_list)
            config.x_labels_major_every = 4
            config.x_label_rotation = 60
        chart = chart_type(config)
        chart.title = title
        for key, value in values.iteritems():
            chart.add(key, value)
        chart.render_to_file(settings.STATIC_ROOT + 'graphs/' + filename)

    def print_progress(self, iteration, total, prefix = 'Progress:', suffix = '', decimals = 2, barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = round(100.00 * (iteration / float(total)), decimals)
        bar             = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
        sys.stdout.flush()
        if iteration == total:
            print("\n")
