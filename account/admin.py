from django.contrib import admin
from schedule.models import ScheduleEntry
from course.models import FollowEntry
from account.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_filter = ('orientation',)

class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False

class ScheduleInline(admin.StackedInline):
    model = ScheduleEntry

class FollowInline(admin.StackedInline):
    model = FollowEntry

class UserAdmin(AuthUserAdmin):
    inlines = [
        ProfileInline,
        ScheduleInline,
        FollowInline,
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
