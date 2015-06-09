from django.contrib import admin
from course.models import Course, Term, Instructor, FollowEntry, Attribute, InstructorLinkSuggestion

admin.site.register(Course)
admin.site.register(Term)
admin.site.register(Instructor)
admin.site.register(FollowEntry)
admin.site.register(Attribute)
admin.site.register(InstructorLinkSuggestion)
