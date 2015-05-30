from django.shortcuts import render, render_to_response
from django.template import RequestContext

def home(request):
    context = {}
    return render(request, 'index.html', context)

def about(request):
    context = {}
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
