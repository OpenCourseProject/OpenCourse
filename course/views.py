from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.mail import mail_admins
from django.utils.safestring import SafeString
from course.models import Course, CourseVersion, Term, FollowEntry, Material, InstructorSuggestion, QueryLog
from schedule.models import ScheduleEntry, ExamEntry, ExamSource
from django_tables2 import RequestConfig
from course.tables import CourseTable
from course.forms import SearchForm, InstructorSuggestionForm
from account.models import Profile
from course.utils import exam_for_course, create_changelog
from django.contrib.auth.decorators import login_required
from tastypie.models import ApiKey
from collections import OrderedDict
import re
import json

def search(request):
    term = None
    crn = None
    course = None
    days = None
    time = None
    instructor = None
    min_rating = None
    attribute = None
    show_closed = True
    if request.method == 'POST':
        form = SearchForm(request.user, request.POST)
        if form.is_valid():
            term = form.cleaned_data['term']
            crn = form.cleaned_data['crn']
            course = form.cleaned_data['course']
            days = form.cleaned_data['days']
            time = form.cleaned_data['time']
            form.fields['time'].initial = time
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
            if 'term' in request.GET:
                term = Term.objects.get(value=request.GET['term'])
        form = SearchForm(request.user)
        form.fields['term'].initial = term
    query = Course.objects.filter(term=term)
    log = {}
    if crn:
        query = query.filter(crn=crn)
        log['crn'] = str(crn)
    if course:
        match = re.search(r'([A-z]+?)([0-9]+)', course)
        if match:
            course = match.group(1) + ' ' + match.group(2)
        query = query.filter(course__icontains=course)
        log['course'] = course
    if days:
        for day in list(days):
            query = query.filter(meeting_times__days__icontains=day)
        log['days'] = days
    if time:
        query = query.filter(meeting_times__start_time=time)
        log['time'] = str(time)
    if instructor:
        query = query.filter(instructor__last_name__icontains=instructor)
        log['instructor'] = instructor
    if min_rating:
        query = query.filter(instructor__rmp_score__gte=min_rating)
        log['min_rating'] = str(min_rating)
    if attribute:
        query = query.filter(attributes__icontains=attribute.value)
        log['attribute'] = str(attribute.value)
    if not show_closed:
        query = query.filter(seats__gt=0)
        log['show_closed'] = show_closed
    query = query.distinct()
    QueryLog.objects.create(user=request.user if request.user.is_authenticated() else None, term=term, data=log, result=query).save()
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
        'suggestion_form': InstructorSuggestionForm(),
    }

    if authenticated:
        user_profile = Profile.objects.get(user=user)
        if not user_profile.private:
            friends = []
            for profile in Profile.objects.all():
                if not profile == user_profile:
                    try:
                        ScheduleEntry.objects.get(user=profile.user, term=term, course_crn=course.crn)
                        friends.append({
                            'first_name': profile.preferred_name if profile.preferred_name else profile.user.first_name,
                            'last_name': profile.user.last_name,
                            'facebook_id': profile.facebook_id
                        })
                    except ScheduleEntry.DoesNotExist:
                        continue
            context['friends'] = json.dumps(friends)

    version_list = CourseVersion.objects.find(course)
    if len(version_list) > 1:
        versions = OrderedDict()
        for i in range(0, len(version_list)-1):
            new_version = version_list[i]
            old_version = version_list[i+1]
            changelog = create_changelog(old_version, new_version)
            if changelog:
                versions[new_version] = changelog
        context['changes'] = versions

    if request.method == 'POST':
        if authenticated:
            form = InstructorSuggestionForm(request.POST)
            if form.is_valid():
                email_address = form.cleaned_data['email_address']
                rmp_link = form.cleaned_data['rmp_link']
                if email_address or rmp_link:
                    suggestion = InstructorSuggestion(instructor=course.instructor, user=user, email_address=email_address, rmp_link=rmp_link)
                    suggestion.save()
                    # Send mail
                    subject = "Instructor suggestion created"
                    message = "{} created a new suggestion for {}: {}, {}".format(request.user.username, course.instructor, email_address, rmp_link)
                    mail_admins(subject, message)
                    context['suggestion_message'] = "Thanks! Your suggestion has been submitted and is awaiting approval."
        else:
            return HttpResponse('Unauthorized', 401)

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
