from django.contrib import admin
from opencourse.models import Report, CourseUpdateLog, EmailLog

class Admin(admin.ModelAdmin):
    readonly_fields = ('time_created',)

admin.site.register(Report, Admin)
admin.site.register(CourseUpdateLog, Admin)
admin.site.register(EmailLog, Admin)
