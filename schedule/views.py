from django.shortcuts import render, redirect
from django.utils.safestring import SafeString
from django.http import Http404
from schedule.models import ScheduleEntry, ExamEntry, ExamSource
from course.models import Term, Course
from account.models import Profile
from django_tables2 import RequestConfig
from schedule.tables import ScheduleTable, ExamTable
from schedule.forms import ScheduleForm
from course.utils import exam_for_course
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import hashlib
import json
import datetime

def schedule(request):
    if not request.user.is_authenticated():
        return redirect('/account/?next=%s' % (request.path))
    else:
        if request.method == 'POST':
            form = ScheduleForm(request.POST)
            if form.is_valid():
                term = form.cleaned_data['term']
        else:
            profile = Profile.objects.get(user=request.user)
            if profile.default_term:
                term = profile.default_term
            else:
                term = Term.objects.all()[0]
            form = ScheduleForm()
            form.fields['term'].initial = term
    query = ScheduleEntry.objects.filter(user=request.user, term=term)
    table = ScheduleTable(schedule_get_courses(query))
    hash = hashlib.md5(b'%s:%s' % (str(request.user.username), str(term.name)))
    share_url = "http://opencourseproject.com/schedule/" + hash.hexdigest()[:15] + "/"

    credits_min = 0
    credits_max = 0
    if len(query) > 0:
        term = query[0].term
        user = query[0].user
        for entry in query:
            value = schedule_get_course(entry).hours
            credits_min += int(value[:1])
            if len(value) > 1:
                credits_max += int(value[4:])
    if credits_max > 0:
        credits_max = credits_min + credits_max

    has_exams = False
    try:
        ExamSource.objects.get(term=term)
        has_exams = True
    except ExamSource.DoesNotExist:
        has_exams = False

    RequestConfig(request).configure(table)
    context = {
        'table': table,
        'form': form,
        'term': term,
        'user': request.user,
        'authenticated': True,
        'by_id': False,
        'share': len(query) > 0,
        'share_url': share_url,
        'credits_min': credits_min,
        'credits_max': credits_max,
        'has_exams': has_exams,
    }
    return render(request, 'schedule/course_schedule.html', context)

def exam_schedule(request, termid):
    if not request.user.is_authenticated():
        return redirect('/account/?next=%s' % (request.path))
    else:
        term = Term.objects.get(value=termid)
        query = ScheduleEntry.objects.filter(user=request.user, term=term)
        exams = []
        for entry in query:
            course = schedule_get_course(entry)
            exam = exam_for_course(course)
            if exam:
                start = exam.exam_start_time
                end = exam.exam_end_time
                exams.append({'course': course.course, 'title': course.title, 'date': exam.exam_date, 'start_time': start, 'end_time': end})

    table = ExamTable(exams)

    RequestConfig(request).configure(table)
    context = {
        'term': term,
        'table': table,
        'user': request.user,
        'authenticated': True,
    }
    return render(request, 'schedule/exam_schedule.html', context)

def schedule_view(request, identifier):
    query = ScheduleEntry.objects.filter(identifier=identifier)
    credits_min = 0
    credits_max = 0
    desc = None
    if len(query) > 0:
        desc = str(len(query)) + (" courses: " if len(query) > 1 else " course: ")
        term = query[0].term
        user = query[0].user
        for entry in query:
            value = entry.course.hours
            desc += entry.course.title + ", "
            credits_min += int(value[:1])
            if len(value) > 1:
                credits_max += int(value[4:])
        desc = desc[:-2]
    else:
        raise Http404("Schedule does not exist")

    if credits_max > 0:
        credits_max = credits_min + credits_max
    courses = schedule_get_courses(query)
    table = ScheduleTable(courses)

    RequestConfig(request).configure(table)
    context = {
        'table': table,
        'social_desc': desc,
        'term': term,
        'user': user,
        'authenticated': False,
        'by_id': True,
        'credits_min': credits_min,
        'credits_max': credits_max,
    }
    return render(request, 'schedule/schedule.html', context)

@login_required
def schedule_add(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if not schedule_check_course(term, course):
            entry = ScheduleEntry(user=request.user, term=term, course_crn=course.crn)
            entry.save()
            return HttpResponse('OK', 201)
        else:
            return HttpResponse('Course is already scheduled', 400)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def schedule_remove(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if schedule_check_course(term, course):
            entry = ScheduleEntry.objects.get(user=request.user, term=term, course_crn=course.crn)
            entry.delete()
            return HttpResponse('OK', 201)
        else:
            return HttpResponse('Course is not scheduled', 400)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def schedule_has(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        course = Course.objects.get(term=term, crn=request.GET['course'])
        if schedule_check_course(term, course):
            return HttpResponse('1', 200)
        else:
            return HttpResponse('0', 200)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def schedule_calendar(request):
    # Requests will include a 'start' value which is a Monday
    delta = datetime.timedelta(days=1)
    MON = datetime.datetime.strptime(request.GET['start'], "%Y-%m-%d")
    TUE = MON + delta
    WED = TUE + delta
    THU = WED + delta
    FRI = THU + delta
    SAT = FRI + delta
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        query = ScheduleEntry.objects.filter(user=request.user, term=term)
        events = []
        for entry in query:
            course = schedule_get_course(entry)
            for day in list(course.days):
                day = MON if day == 'M' else TUE if day == 'T' else WED if day == 'W' else THU if day == 'R' else FRI if day == 'F' else SAT
                start = datetime.datetime.combine(day, course.start_time).isoformat()
                end = datetime.datetime.combine(day, course.end_time).isoformat()
                events.append({
                    'id': str(course.crn),
                    'title': course.course,
                    'start': start,
                    'end': end,
                    'url': 'http://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/',
                })
        days = SafeString(json.dumps(events))
        return HttpResponse(days, 201)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def exam_calendar(request):
    if request.method == 'GET':
        term = Term.objects.get(value=request.GET['term'])
        query = ScheduleEntry.objects.filter(user=request.user, term=term)
        events = []
        for entry in query:
            course = schedule_get_course(entry)
            exam = exam_for_course(course)
            if exam:
                start = datetime.datetime.combine(exam.exam_date, exam.exam_start_time).isoformat()
                end = datetime.datetime.combine(exam.exam_date, exam.exam_start_time).isoformat()
                events.append({
                    'id': str(course.crn),
                    'title': course.course,
                    'start': start,
                    'end': end,
                    'url': 'http://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/',
                })
        exams = SafeString(json.dumps(events))
        return HttpResponse(exams, 201)
    else:
        return HttpResponse('Method not allowed', 405)

def schedule_check_course(term, course):
    entries = ScheduleEntry.objects.filter(term=term, course_crn=course.crn)
    return len(entries) > 0

def schedule_get_course(entry):
    return Course.objects.get(term=entry.term, crn=entry.course_crn)

def schedule_get_courses(entries):
    courses = []
    for entry in entries:
        courses.append(schedule_get_course(entry))
    return courses
