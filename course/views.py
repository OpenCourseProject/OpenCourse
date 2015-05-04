from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from course.models import Course, Term, FollowEntry
from schedule.models import ScheduleEntry, ExamEntry, ExamSource
from django.template import RequestContext
from django_tables2 import RequestConfig
from course.tables import CourseTable
from course.forms import SearchForm
from account.models import Profile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import logging

logging.basicConfig()

def home(request):
    context = {}
    return render(request, 'index.html', context)

def error_500(request):
    context = RequestContext(request)
    if request.path == '/complete/google-oauth2/':
        response = render_to_response('account/500_login.html', {}, context)
    else:
        response = render_to_response('500.html', {}, context)
    response.status_code = 500
    return response

def error_404(request):
    context = RequestContext(request)
    if request.path.startswith('/schedule/'):
        response = render_to_response('schedule/404.html', {}, context)
    else:
        response = render_to_response('404.html', {}, context)
    response.status_code = 404
    return response

def search(request):
    crn = None
    course = None
    days = None
    start = None
    end = None
    instructor = None
    min_rating = None
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
        query = query.filter(days=days)
    if start:
        query = query.filter(start_time=start)
    if end:
        query = query.filter(end_time=end)
    if instructor:
        query = query.filter(instructor__last_name__icontains=instructor)
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

    exams = ExamEntry.objects.filter(term=term, course_start_time=course.start_time, course_end_time=course.end_time)

    if course.days == "T" or course.days == "R":
        exams = exams.filter(Q(days=course.days) | Q(days="T/R"))
    elif course.days == "M" or course.days == "W":
        exams = exams.filter(Q(days=course.days) | Q(days="M/W") | Q(days="M/W/F"))
    else:
        exams = exams.filter(days=course.days)

    exam = None
    if len(exams) == 1:
        exam = exams[0]

    exam_sources = ExamSource.objects.filter(term=term)
    exam_source = None
    if len(exam_sources) == 1:
        exam_source = exam_sources[0]

    user = request.user
    authenticated = user.is_authenticated()
    context = {
        'course': course,
        'term': term,
        'authenticated': authenticated,
        'user': user,
        'exam': exam,
        'exam_source': exam_source,
    }
    return render(request, 'course/course.html', context)

@login_required
def follow_add(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if not follow_check_course(term, course):
            entry = FollowEntry(user=request.user, term=term, course=course)
            entry.save()
            return HttpResponse('OK', 201)
        else:
            return HttpResponse('User is already following', 400)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def find_friends(request):
    if request.method == 'GET':
        course = Course.objects.get(term=request.GET['term'], crn=request.GET['crn'])
        friends = []
        for profile in Profile.objects.filter(facebook_id__isnull=False):
            facebook_id = profile.facebook_id
            user = profile.user
            try:
                ScheduleEntry.objects.get(user=user, course=course)
                friends.append(facebook_id)
            except ScheduleEntry.DoesNotExist:
                continue
        return HttpResponse(','.join(friends), 201)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def follow_remove(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if follow_check_course(term, course):
            entry = FollowEntry.objects.get(user=request.user, term=term, course=course)
            entry.delete()
            return HttpResponse('OK', 201)
        else:
            return HttpResponse('User is not following', 400)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def follow_has(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if follow_check_course(term, course):
            return HttpResponse('1', 200)
        else:
            return HttpResponse('0', 200)
    else:
        return HttpResponse('Method not allowed', 405)

def follow_check_course(term, course):
    entries = FollowEntry.objects.filter(term=term, course=course)
    return len(entries) > 0
