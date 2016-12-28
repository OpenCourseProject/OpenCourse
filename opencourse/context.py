from opencourse.forms import ReportForm
from tastypie.models import ApiKey
from django.conf import settings
from course.models import Term
from account.models import Profile

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

def school_info(request):
    return {
        'school_name': settings.SCHOOL_NAME,
        'school_abbr': settings.SCHOOL_ABBREVIATION,
        'school_website': settings.SCHOOL_WEBSITE,
    }

def domain(request):
    return {
        'domain': request.get_host(),
        'domain_full': ('https://' if request.is_secure() else 'http://') + request.get_host()
    }

def update_interval(request):
    return {
        'course_interval': settings.COURSE_UPDATE_INTERVAL,
        'material_interval': settings.MATERIAL_UPDATE_INTERVAL,
        'rating_interval': settings.RATING_UPDATE_INTERVAL
    }

def term_info(request):
    return {
        'current_term': Term.objects.get(value=settings.CURRENT_TERM),
        'sync_term': Term.objects.get(value=settings.SYNC_TERM)
    }

def user_info(request):
    context = {}
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        context['profile'] = profile
    return context
