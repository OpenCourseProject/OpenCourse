from opencourse.forms import ReportForm
from tastypie.models import ApiKey

def report(request):
    return {'report_form': ReportForm()}

def api(request):
    if request.user.is_authenticated():
        return {
            'api_username': request.user.username,
            'api_key': ApiKey.objects.get(user=request.user).key,
        }
    else:
        return {}
