from django.contrib import admin
from course.models import Course, CourseVersion, Term, Instructor, FollowEntry, Attribute, InstructorSuggestion, QueryLog

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['crn', 'course', 'title']

class CourseInline(admin.StackedInline):
    model = Course

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    search_fields = ['last_name']

@admin.register(FollowEntry)
class FollowEntryAdmin(admin.ModelAdmin):
    search_fields = ['course_crn', 'user__username']

admin.site.register(CourseVersion)
admin.site.register(Term)
admin.site.register(Attribute)
admin.site.register(InstructorSuggestion)
admin.site.register(QueryLog)
