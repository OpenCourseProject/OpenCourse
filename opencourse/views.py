from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.safestring import SafeString
from account.models import Profile
from schedule.models import ScheduleEntry
from course.models import FollowEntry

def home(request):
    todo = []
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        if not profile.facebook_id:
            todo.append(SafeString('<a href="/account/#facebook">Login with Facebook to find friends in your classes</a>'))
        entries = ScheduleEntry.objects.filter(user=request.user)
        if len(entries) == 0:
            todo.append(SafeString('<a href="/search/">Start adding courses to your schedule</a>'))
        else:
            todo.append(SafeString('<a href="https://www.facebook.com/sharer/sharer.php?u=https://opencourseproject.com/schedule/' + entries[0].identifier + '/&t=' + entries[0].term.name + ' schedule for ' + request.user.first_name + ' ' + request.user.last_name + '"onclick="javascript:window.open(this.href, '', \'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600\');return false;"target="_blank">Share a schedule on social media</a>'))
        entries = FollowEntry.objects.filter(user=request.user)
        if len(entries) == 0:
            todo.append(SafeString('<a href="/search/">Follow a course to get status updates</a>'))
        todo.append(SafeString('<a href="https://github.com/gravitylow/OpenCourse/issues">Send a suggestion or a bug report</a>'))
    context = {
        'user': request.user,
        'todo': todo,
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'user': request.user,
    }
    return render(request, 'about.html', context)

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
