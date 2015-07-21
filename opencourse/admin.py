from django.contrib import admin
from opencourse.models import Report, CourseUpdateLog, EmailLog

@admin.register(CourseUpdateLog, EmailLog)
class Admin(admin.ModelAdmin):
    readonly_fields = ('time_created',)

@admin.register(Report)
class ReportAdmin(Admin):
    list_filter = ('responded', 'time_created',)
