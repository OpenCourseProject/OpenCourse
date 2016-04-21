from django.http import JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.safestring import SafeString
from django.core.mail import mail_admins
from account.models import Profile
from schedule.models import ScheduleEntry
from schedule.utils import schedule_get_course
from course.models import Course, Term, FollowEntry, CourseVersion, QueryLog
from course.utils import course_create_changelog
from opencourse.models import Report, Alert
from opencourse.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count
from collections import OrderedDict

def home(request):
    current_term = Term.objects.get(value=201700)
    query = ScheduleEntry.objects.filter(term_id=current_term.value).values('course_crn').annotate(Count('course_crn')).order_by('-course_crn__count')[:3]
    popular_courses = OrderedDict()
    alerts = Alert.objects.all()
    context = {
        'current_term': current_term,
        'popular_courses': popular_courses,
        'alerts': alerts,
    }
    for entry in query:
        popular_courses[Course.objects.get(term=current_term, crn=entry['course_crn'])] = entry['course_crn__count']
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        todo = []
        if not profile.facebook_id:
            todo.append(SafeString('<a href="/account/#facebook">Login with Facebook to find friends in your classes</a>'))
        if not profile.learning_community:
            todo.append(SafeString('<a href="/account/#profile">Add your Learning Community to share on your schedules</a>'))
        entries = ScheduleEntry.objects.filter(user=request.user)
        if len(entries) == 0:
            todo.append(SafeString('<a href="/search/">Start adding courses to your schedule</a>'))
        else:
            todo.append(SafeString('<a href="https://www.facebook.com/sharer/sharer.php?u=https://opencourseproject.com/schedule/' + entries[0].identifier + '/&t=' + entries[0].term.name + ' schedule for ' + request.user.first_name + ' ' + request.user.last_name + ' "onclick="javascript:window.open(this.href, '', \'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600\');return false;" target="_blank">Share a schedule on social media</a>'))
        entries = FollowEntry.objects.filter(user=request.user)
        if len(entries) == 0:
            todo.append(SafeString('<a href="/search/">Follow a course to get status updates</a>'))
        todo.append(SafeString('<a href="#report" data-toggle="modal" data-target="#report">Send a suggestion or a bug report</a>'))
        context['todo'] = todo
        context['first_name'] = profile.preferred_name if profile.preferred_name else request.user.first_name
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

@login_required
def report(request):
    context = {}
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']
            report = Report(user=request.user, url=url, description=description)
            report.save()
            # Send mail
            subject = "Report created"
            message = "{} created a new report on {}: {}".format(request.user.username, url, description)
            mail_admins(subject, message)
            context = {
                'report': report,
            }
            return render(request, 'report.html', context)
    return redirect('/')

@csrf_protect
def error_500(request):
    if request.path == '/complete/google-oauth2/':
        response = render(request, 'account/500_login.html', {})
    else:
        response = render(request, '500.html', {})
    response.status_code = 500
    return response

@csrf_protect
def error_404(request):
    if request.path.startswith('/schedule/'):
        response = render(request, 'schedule/404.html', {})
    else:
        response = render(request, '404.html', {})
    response.status_code = 404
    return response
