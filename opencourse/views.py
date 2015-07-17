from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.safestring import SafeString
from account.models import Profile
from schedule.models import ScheduleEntry
from schedule.utils import schedule_get_course
from course.models import Course, Term, FollowEntry
from opencourse.models import Report
from opencourse.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import OrderedDict

def home(request):
    todo = []
    current_term = Term.objects.get(value=201600)
    query = ScheduleEntry.objects.filter(term_id=current_term.value).values('course_crn').annotate(Count('course_crn')).order_by('-course_crn__count')[:3]
    popular_courses = OrderedDict()
    for entry in query:
        popular_courses[Course.objects.get(term=current_term, crn=entry['course_crn'])] = entry['course_crn__count']
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
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
    context = {
        'todo': todo,
        'current_term': current_term,
        'popular_courses': popular_courses,
    }
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
            context = {
                'report': report,
            }
            return render(request, 'report.html', context)
    return redirect('/')

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
