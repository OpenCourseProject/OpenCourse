import django_tables2 as tables
from course.models import Course

class CourseTable(tables.Table):
    class Meta:
        model = Course
        template = "course/table.html"
        empty_text = "No courses found for this term"
        attrs = {"class": "table table-bordered table-striped table-hover"}
        fields = ("crn", "course", "title", "hours", "attributes", "ctype", "days", "start_time", "end_time", "location", "instructor", "seats")
