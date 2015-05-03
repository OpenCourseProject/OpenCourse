import django_tables2 as tables
from course.models import Course

class ScheduleTable(tables.Table):
    class Meta:
        model = Course
        template = "schedule/table.html"
        order_by = "start_time"
        empty_text = "No courses yet!"
        attrs = {"class": "table table-bordered table-striped table-hover"}
        fields = ("crn", "course", "section", "title", "hours", "llc", "ctype", "days", "start_time", "end_time", "location", "instructor", "seats")
