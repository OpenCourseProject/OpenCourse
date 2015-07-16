from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from course.models import Course, Term, FollowEntry, Material, InstructorLinkSuggestion
from schedule.models import ScheduleEntry, ExamEntry, ExamSource
from django_tables2 import RequestConfig
from course.tables import CourseTable
from course.forms import SearchForm, InstructorSuggestionForm
from account.models import Profile
from course.utils import exam_for_course
from django.contrib.auth.decorators import login_required
from tastypie.models import ApiKey
import json
import logging

logging.basicConfig()

def search(request):
    term = None
    crn = None
    course = None
    days = None
    start = None
    end = None
    instructor = None
    min_rating = None
    attribute = None
    show_closed = True
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['term']
            crn = form.cleaned_data['crn']
            course = form.cleaned_data['course']
            days = form.cleaned_data['days']
            start = form.cleaned_data['start']
            form.fields['start'].initial = start
            end = form.cleaned_data['end']
            form.fields['end'].initial = start
            instructor = form.cleaned_data['instructor']
            min_rating = form.cleaned_data['min_rating']
            attribute = form.cleaned_data['attribute']
            show_closed = form.cleaned_data['show_closed']
    else:
        term = Term.objects.all()[0]
        if request.user.is_authenticated():
            profile = Profile.objects.get(user=request.user)
            if profile.default_term:
                term = profile.default_term
        form = SearchForm()
        form.fields['term'].initial = term
    query = Course.objects.filter(term=term)
    if crn:
        query = query.filter(crn=crn)
    if course:
        query = query.filter(course__icontains=course)
    if days:
        for day in list(days):
            query = query.filter(meeting_times__days__icontains=day)
    if start:
        query = query.filter(meeting_times__start_time=start)
    if end:
        query = query.filter(meeting_times__end_time=end)
    if instructor:
        query = query.filter(instructor__last_name__icontains=instructor)
    if min_rating:
        query = query.filter(instructor__rmp_score__gte=min_rating)
    if attribute:
        query = query.filter(attributes__icontains=attribute.value)
    if not show_closed:
        query = query.filter(seats__gt=0)
    table = CourseTable(query)

    RequestConfig(request).configure(table)
    context = {'table' : table, 'form' : form, 'term': term}
    return render(request, 'course/search.html', context)

def course(request, term, crn):
    try:
        term = Term.objects.get(value=term)
        course = Course.objects.get(term=term, crn=crn)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")

    materials = Material.objects.filter(term=term, course_crn=course.crn)

    user = request.user
    authenticated = user.is_authenticated()

    context = {
        'course': course,
        'term': term,
        'authenticated': authenticated,
        'user': user,
        'materials': materials,
    }

    if authenticated:
        api_key = ApiKey.objects.get(user=request.user)
        context['api_key'] = api_key

        if request.method == 'POST':
            form = InstructorSuggestionForm(request.POST)
            if form.is_valid():
                link = form.cleaned_data['link']
                suggestion = InstructorLinkSuggestion(instructor=course.instructor, user=user, link=link)
                suggestion.save()
        else:
            context['suggestion_form'] = InstructorSuggestionForm()

    primary = course.primary_meeting_time
    secondary = course.secondary_meeting_times
    if primary:
        context['primary_meeting_time'] = primary
    if secondary:
        context['secondary_meeting_times'] = secondary

    exam = exam_for_course(course)
    exam_sources = ExamSource.objects.filter(term=term)
    if exam:
        context['exam'] = exam
    if len(exam_sources) == 1:
        context['exam_source'] = exam_sources[0]

    return render(request, 'course/course.html', context)

@login_required
def find_friends(request):
    if request.method == 'GET':
        course = Course.objects.get(term=request.GET['term'], crn=request.GET['crn'])
        friends = []
        for profile in Profile.objects.filter(facebook_id__isnull=False):
            facebook_id = profile.facebook_id
            user = profile.user
            try:
                ScheduleEntry.objects.get(user=user, course_crn=course.crn)
                friends.append(facebook_id)
            except ScheduleEntry.DoesNotExist:
                continue
        return HttpResponse(','.join(friends), 201)
    else:
        return HttpResponse('Method not allowed', 405)
