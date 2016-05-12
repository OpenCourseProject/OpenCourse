from django.shortcuts import render
from django.conf import settings
from course.models import Term, Course, CourseVersion, FollowEntry, QueryLog
from course.utils import course_create_changelog
from opencourse.models import TermUpdate, UpdateLog
from schedule.models import ScheduleEntry

def dashboard(request):
    current_term = Term.objects.get(value=settings.CURRENT_TERM)
    context = {
        'current_term': current_term,
        'terms': Term.objects.all(),
        'courses': Course.objects.all(),
        'schedule_entries': ScheduleEntry.objects.all(),
        'follow_entries': FollowEntry.objects.all(),
        'course_versions': CourseVersion.objects.all(),
        'query_logs': QueryLog.objects.all(),
    }
    return render(request, 'dashboard/dashboard.html', context)

def changes(request):
    current_term = Term.objects.get(value=settings.CURRENT_TERM)
    changes = []
    versions = CourseVersion.objects.all().order_by('-time_created')[:10]
    for version in versions:
        course = Course.objects.get(crn=version.course_crn, term=version.term)
        changelog = course_create_changelog(course)
        changes.append({
            'url': course.url,
            'course': course,
            'changes': changelog,
            'time': version.time_created
        })
    context = {
        'current_term': current_term,
        'changes': changes,
    }
    return render(request, 'dashboard/changes.html', context)

def events(request):
    events = []
    follows = FollowEntry.objects.all().order_by('-time_created')[:10]
    for follow in follows:
        course = Course.objects.get(crn=follow.course_crn, term=follow.term)
        events.append({
            'text': 'Someone followed {}.'.format('<a href="{}">{}</a>'.format(course.url, course)),
            'time': follow.time_created
        })
    schedules = ScheduleEntry.objects.all().order_by('-time_created')[:10]
    for schedule in schedules:
        course = Course.objects.get(crn=schedule.course_crn, term=schedule.term)
        events.append({
            'text': 'Someone added {} to their schedule.'.format('<a href="{}">{}</a>'.format(course.url, course)),
            'time': schedule.time_created
        })
    events = sorted(events, key=sort_by_time, reverse=True)[:10]
    context = {
        'events': events,
    }
    return render(request, 'dashboard/events.html', context)

def courses(request):
    current_term = Term.objects.get(value=settings.CURRENT_TERM)
    courses = []
    if request.user.is_authenticated():
        scheduled_courses = ScheduleEntry.objects.filter(user=request.user, term=current_term)
        for schedule in scheduled_courses:
            course = Course.objects.get(crn=schedule.course_crn, term=schedule.term)
            versions = (CourseVersion.objects.find(course)[:2])
            last_version = versions[1] if len(versions) is 2 else versions[0]
            values = {
                'current': course,
                'last': last_version.field_list(),
                'last_time': last_version.time_created
            }
            courses.append(values)
    context = {
        'courses': courses,
    }
    return render(request, 'dashboard/courses.html', context)

def sort_by_time(obj):
    return obj['time']

def updates(request):
    updates = UpdateLog.objects.all().order_by('-time_created')[:5]
    terms = Term.objects.all()
    context = {
        'updates': updates,
        'terms': terms,
    }
    return render(request, 'dashboard/updates.html', context)
