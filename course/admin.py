from django.contrib import admin
from course.models import Course, Term, Instructor, FollowEntry, Attribute, InstructorLinkSuggestion

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['crn', 'course', 'title']

class CourseInline(admin.StackedInline):
    model = Course

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    search_fields = ['last_name']
    inlines = [
        CourseInline,
    ]

@admin.register(FollowEntry)
class FollowEntryAdmin(admin.ModelAdmin):
    search_fields = ['course_crn', 'user__username']

admin.site.register(Term)
admin.site.register(Attribute)
admin.site.register(InstructorLinkSuggestion)
