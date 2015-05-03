from django.contrib import admin
from schedule.models import ScheduleEntry, ExamEntry, ExamSource

admin.site.register(ScheduleEntry)
admin.site.register(ExamEntry)
admin.site.register(ExamSource)
