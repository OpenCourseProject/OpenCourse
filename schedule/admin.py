from django.contrib import admin
from schedule.models import ScheduleEntry, ExamEntry, ExamSource

@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    search_fields = ['course_crn', 'user__username']

admin.site.register(ExamEntry)
admin.site.register(ExamSource)
