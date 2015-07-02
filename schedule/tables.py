import django_tables2 as tables
from course.models import Course

class ScheduleTable(tables.Table):
    days = tables.Column(accessor='primary_meeting_time.days', order_by='meeting_times.days')
    start_time = tables.Column(accessor='primary_meeting_time.start_time', order_by='meeting_times.start_time')
    end_time = tables.Column(accessor='primary_meeting_time.end_time', order_by='meeting_times.end_time')

    class Meta:
        model = Course
        template = "schedule/course_table.html"
        order_by = "start_time"
        empty_text = "No courses yet!"
        attrs = {"class": "table table-bordered table-striped table-hover"}
        fields = ("crn", "course", "section", "title", "hours", "llc", "ctype", "days", "start_time", "end_time", "location", "instructor", "seats")

class ExamTable(tables.Table):
    course = tables.Column()
    crn = tables.Column(verbose_name='CRN')
    title = tables.Column()
    date = tables.DateColumn()
    start_time = tables.TimeColumn()
    end_time = tables.TimeColumn()

    class Meta:
        template = "schedule/exam_table.html"
        order_by = "date"
        empty_text = "No exams found for your schedule"
        attrs = {"class": "table table-bordered table-striped table-hover"}
