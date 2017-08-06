import django_tables2 as tables
from course.models import Course
from django.utils.safestring import mark_safe

class CourseTable(tables.Table):
    days = tables.Column(accessor='primary_meeting_time.days', order_by='meeting_times.days')
    start_time = tables.Column(accessor='primary_meeting_time.start_time', order_by='meeting_times.start_time')
    end_time = tables.Column(accessor='primary_meeting_time.end_time', order_by='meeting_times.end_time')

    class Meta:
        model = Course
        template = "course/table.html"
        empty_text = "No courses found for this term"
        attrs = {"class": "table table-bordered table-striped table-hover"}
        fields = ("crn", "course", "title", "hours", "attributes", "ctype", "days", "start_time", "end_time", "location", "instructor", "seats")

    def render_title(self, value, record):
        if record.deleted:
            return mark_safe('<del>{}</del>'.format(value))
        else:
            return mark_safe('{}'.format(value))

    def render_course(self, value, record):
        if record.deleted:
            return mark_safe('<del>{}</del>'.format(value))
        else:
            return mark_safe('{}'.format(value))
