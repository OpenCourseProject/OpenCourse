from django.contrib import admin
from schedule.models import ScheduleEntry, ScheduleTransaction, ExamEntry, ExamSource

@admin.register(ScheduleEntry, ScheduleTransaction)
class ScheduleEntryAdmin(admin.ModelAdmin):
    search_fields = ['course_crn', 'user__username']

admin.site.register(ExamEntry)
admin.site.register(ExamSource)
