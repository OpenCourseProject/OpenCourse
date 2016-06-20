from django.conf.urls import patterns, include, url

from django.contrib import admin
from opencourse.views import home, about, start, start_setup, report, error_500, error_404
admin.autodiscover()

from tastypie.api import Api
from api.resources import CourseResource, TermResource, InstructorResource, AttributeResource, MaterialResource, CourseVersionResource, ScheduleResource, FollowResource, ProfileResource

v1_api = Api(api_name='v1')
v1_api.register(CourseResource())
v1_api.register(TermResource())
v1_api.register(InstructorResource())
v1_api.register(AttributeResource())
v1_api.register(MaterialResource())
v1_api.register(CourseVersionResource())
v1_api.register(ScheduleResource())
v1_api.register(FollowResource())
v1_api.register(ProfileResource())

handler500 = error_500
handler404 = error_404

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^', include('course.urls', namespace="search")),
    url(r'^about/', about, name='about'),
    url(r'^start/$', start, name='start'),
    url(r'^start/setup/', start_setup, name='start setup'),
    url(r'^api/', include('api.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^schedule/', include('schedule.urls', namespace="schedule")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^updates/', include('updates.urls', namespace="updates")),
    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
    url(r'^orientation/', include('orientation.urls', namespace="orientation")),
    # Third-party urls
    url('', include('social.apps.django_app.urls', namespace='social')),
    # Internal API
    url(r'^report/', report, name='report'),
)
