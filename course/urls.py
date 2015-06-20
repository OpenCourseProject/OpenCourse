from django.conf.urls import patterns, url

from course import views

urlpatterns = patterns('',
    url(r'^search/$', views.search, name='search'),
    url(r'^friends/$', views.find_friends, name='find facebook friends'),
    url(r'^course/(?P<term>(\d+))/(?P<crn>(\d+))/$', views.course, name='course'),
)
