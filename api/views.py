from django.shortcuts import render
from tastypie.models import ApiKey
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    if request.user.is_authenticated():
        context['user'] = request.user
        try:
            context['api_key'] = ApiKey.objects.get(user=request.user)
        except ApiKey.DoesNotExist:
            pass
    return render(request, 'api/index.html', context)

@login_required
def api_username(request):
    if request.method == 'GET':
        return HttpResponse(request.user.username, 200)
    else:
        return HttpResponse('Method not allowed', 405)

@login_required
def api_key(request):
    if request.method == 'GET':
        key = ApiKey.objects.get(user=request.user)
        return HttpResponse(key.key, 200)
    else:
        return HttpResponse('Method not allowed', 405)
