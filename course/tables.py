import django_tables2 as tables
from course.models import Course
from django.utils.safestring import mark_safe
from django.utils import dateformat

class CourseTable(tables.Table):
    days = tables.Column(accessor='primary_meeting_time.days', order_by='meeting_times.days')
    start_time = tables.Column(accessor='primary_meeting_time.start_time', order_by='meeting_times.start_time')
    end_time = tables.Column(accessor='primary_meeting_time.end_time', order_by='meeting_times.end_time')

    class Meta:
        model = Course
        template = "course/table.html"
        empty_text = "No courses found for this term"
        attrs = {"class": "table table-bordered table-striped table-hover", "style": "width: 100%"}
        fields = ("crn", "course", "title", "hours", "attributes", "ctype", "days", "start_time", "end_time", "location", "instructor", "seats")

    def render_crn(self, value, record):
        return self.make_link(value, record)

    def render_title(self, value, record):
        return self.make_link(value, record)

    def render_course(self, value, record):
        return self.make_link(value, record)

    def render_hours(self, value, record):
        return self.make_link(value, record)

    def render_attributes(self, value, record):
        return self.make_link(value, record)

    def render_ctype(self, value, record):
        return self.make_link(value, record)

    def render_days(self, value, record):
        return self.make_link(value, record)

    def render_start_time(self, value, record):
        return self.make_link(dateformat.format(value, 'P'), record)

    def render_end_time(self, value, record):
        return self.make_link(dateformat.format(value, 'P'), record)

    def render_location(self, value, record):
        return self.make_link(value, record)

    def render_instructor(self, value, record):
        if record.instructor.rmp_link:
            text = '<a href="{}">{}</a>'.format(record.instructor.rmp_link, value)
            if record.deleted:
                text = '<del>{}</del>'.format(text)
            return mark_safe(text)
        else:
            return self.make_link(value, record)

    def render_seats(self, value, record):
        return self.make_link(value, record)

    def make_link(self, value, record):
        text = '<a class="silent" href="{}">{}</a>'.format(record.url, value)
        if record.deleted:
            text = '<del>{}</del>'.format(text)
        return mark_safe(text)
