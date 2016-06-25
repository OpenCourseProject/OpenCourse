from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from orientation.forms import SearchForm
from account.models import Profile
from schedule.models import ScheduleEntry
from schedule.utils import schedule_get_courses
import re

@login_required
def search(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.orientation:
        return HttpResponseForbidden()
    results = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_course = form.cleaned_data['course']
            search_instructor = form.cleaned_data['instructor']
            profiles = Profile.objects.filter(orientation=True)
            for profile in profiles:
                courses = schedule_get_courses(ScheduleEntry.objects.filter(user=profile.user))
                for course in courses:
                    add = False
                    if search_course:
                        match = re.search(r'([A-z]+?)([0-9]+)', search_course)
                        if match:
                            search_course = match.group(1) + ' ' + match.group(2)
                        if search_course in course.course:
                            add = True
                        else:
                            add = False
                    if search_instructor:
                        if search_instructor in course.instructor.last_name:
                            add = True
                        else:
                            add = False
                    if add:
                        results.append({
                            'user': profile.user,
                            'profile': profile,
                            'course': course
                        })
    else:
        form = SearchForm()
    context = {
        'results': results,
        'form' : form
    }
    return render(request, 'orientation/search.html', context)

@login_required
def majors(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.orientation:
        return HttpResponseForbidden()
    results = []
    profiles = Profile.objects.filter(orientation=True)
    context = {
        'profiles': profiles
    }
    return render(request, 'orientation/majors.html', context)
