from django.shortcuts import render
from django.utils.safestring import SafeString
from django.http import Http404
from schedule.models import ScheduleEntry, ExamEntry, ExamSource
from schedule.utils import schedule_get_course, schedule_get_courses
from course.models import Term, Course
from account.models import Profile
from django_tables2 import RequestConfig
from schedule.tables import ScheduleTable, SchedulePrintTable, ExamTable
from schedule.forms import ScheduleForm
from course.utils import exam_for_course
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import hashlib
import json
import datetime

@login_required
def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data['term']
    else:
        if 'term' in request.GET:
            term = Term.objects.get(value=request.GET['term'])
        else:
            profile = Profile.objects.get(user=request.user)
            if profile.default_term:
                term = profile.default_term
            else:
                term = Term.objects.all()[0]
        form = ScheduleForm()
        form.fields['term'].initial = term
    query = ScheduleEntry.objects.filter(user=request.user, term=term)
    courses = schedule_get_courses(query)
    hash = hashlib.md5(b'%s:%s' % (str(request.user.username), str(term.name))).hexdigest()[:15]
    share_url = "https://opencourseproject.com/schedule/" + hash + "/"

    credits_min = 0
    credits_max = 0
    invalid_courses = []
    if len(query) > 0:
        term = query[0].term
        user = query[0].user
        for entry in query:
            course = schedule_get_course(entry)
            if course is None:
                invalid_courses.append(entry)
                courses.remove(course)
            else:
                value = course.hours
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

    table = ScheduleTable(courses)
    print_table = SchedulePrintTable(courses)
    RequestConfig(request).configure(table)
    RequestConfig(request).configure(print_table)
    context = {
        'table': table,
        'print_table': print_table,
        'form': form,
        'term': term,
        'authenticated': True,
        'by_id': False,
        'identifier': hash,
        'share': len(query) > 0,
        'share_url': share_url,
        'credits_min': credits_min,
        'credits_max': credits_max,
        'invalid_courses': invalid_courses,
        'has_exams': has_exams,
    }
    return render(request, 'schedule/course_schedule.html', context)

@login_required
def exam_schedule(request, termid):
    term = Term.objects.get(value=termid)
    query = ScheduleEntry.objects.filter(user=request.user, term=term)
    courses = schedule_get_courses(query)
    exams = []
    first_exam = None
    for course in courses:
        if course is None:
            courses.remove(course)
        else:
            exam = exam_for_course(course)
            if exam:
                start = exam.exam_start_time
                end = exam.exam_end_time
                exams.append({
                    'course': course.course,
                    'crn': course.crn,
                    'title': course.title,
                    'date': exam.exam_date,
                    'start_time': start,
                    'end_time': end
                })
                if not first_exam or exam.exam_date < first_exam:
                    first_exam = exam.exam_date

    hash = hashlib.md5(b'%s:%s' % (str(request.user.username), str(term.name))).hexdigest()[:15]

    table = ExamTable(exams)

    RequestConfig(request).configure(table)
    context = {
        'source': ExamSource.objects.get(term=term),
        'term': term,
        'table': table,
        'first_exam': first_exam.strftime('%Y-%m-%d'),
        'identifier': hash,
        'authenticated': True,
    }
    return render(request, 'schedule/exam_schedule.html', context)

def schedule_view(request, identifier):
    query = ScheduleEntry.objects.filter(identifier=identifier)
    courses = schedule_get_courses(query)
    credits_min = 0
    credits_max = 0
    desc = None
    if len(query) > 0:
        desc = str(len(query)) + (" courses: " if len(query) > 1 else " course: ")
        term = query[0].term
        user = query[0].user
        profile = Profile.objects.get(user=user)
        for course in courses:
            if course is None:
                courses.remove(course)
            else:
                value = course.hours
                desc += course.title + ", "
                credits_min += int(value[:1])
                if len(value) > 1:
                    credits_max += int(value[4:])
        desc = desc[:-2]
    else:
        raise Http404("Schedule does not exist")

    if credits_max > 0:
        credits_max = credits_min + credits_max
    table = ScheduleTable(courses)

    RequestConfig(request).configure(table)

    context = {
        'table': table,
        'social_desc': desc,
        'term': term,
        'schedule_user': user,
        'schedule_profile': profile,
        'by_id': True,
        'identifier': identifier,
        'credits_min': credits_min,
        'credits_max': credits_max,
    }

    if user != request.user and request.user.is_authenticated():
        context['user_courses'] = schedule_get_courses(ScheduleEntry.objects.filter(user=request.user))
        context['profile'] = Profile.objects.get(user=request.user)

    return render(request, 'schedule/course_schedule.html', context)

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
        query = ScheduleEntry.objects.filter(identifier=request.GET['identifier'])
        events = []
        for entry in query:
            course = schedule_get_course(entry)
            for meeting_time in course.meeting_times.all():
                for day in list(meeting_time.days):
                    day = MON if day == 'M' else TUE if day == 'T' else WED if day == 'W' else THU if day == 'R' else FRI if day == 'F' else SAT
                    start = datetime.datetime.combine(day, meeting_time.start_time).isoformat()
                    end = datetime.datetime.combine(day, meeting_time.end_time).isoformat()
                    events.append({
                        'id': str(course.crn),
                        'title': course.course,
                        'start': start,
                        'end': end,
                        'url': 'https://opencourseproject.com/course/' + str(course.term.value) + '/' + str(course.crn) + '/',
                    })
        days = SafeString(json.dumps(events))
        return HttpResponse(days, 201)
    else:
        return HttpResponse('Method not allowed', 405)

def exam_calendar(request):
    if request.method == 'GET':
        query = ScheduleEntry.objects.filter(identifier=request.GET['identifier'])
        events = []
        for entry in query:
            course = schedule_get_course(entry)
            exam = exam_for_course(course)
            if exam:
                start = datetime.datetime.combine(exam.exam_date, exam.exam_start_time).isoformat()
                end = datetime.datetime.combine(exam.exam_date, exam.exam_end_time).isoformat()
                events.append({
                    'id': str(course.crn),
                    'title': course.course,
                    'start': start,
                    'end': end,
                    'url': 'https://opencourseproject.com/course/' + str(course.term.value) + '/' + str(course.crn) + '/',
                })
        exams = SafeString(json.dumps(events))
        return HttpResponse(exams, 201)
    else:
        return HttpResponse('Method not allowed', 405)
