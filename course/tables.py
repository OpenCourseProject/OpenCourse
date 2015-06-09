import django_tables2 as tables
from course.models import Course

class CourseTable(tables.Table):
    rating = tables.Column(accessor='instructor.rmp_score')
    days = tables.Column(accessor='primary_meeting_time.days', order_by='meeting_times.days')
    start_time = tables.Column(accessor='primary_meeting_time.start_time', order_by='meeting_times.start_time')
    end_time = tables.Column(accessor='primary_meeting_time.end_time', order_by='meeting_times.end_time')

    class Meta:
        model = Course
        template = "course/table.html"
        empty_text = "No courses found for this term"
        attrs = {"class": "table table-bordered table-striped table-hover"}
        fields = ("crn", "course", "title", "hours", "attributes", "ctype", "days", "start_time", "end_time", "location", "instructor", "rating", "seats")
