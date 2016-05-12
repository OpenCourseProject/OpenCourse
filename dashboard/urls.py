from django.conf.urls import patterns, url

from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^changes/$', views.changes, name='changes'),
    url(r'^events/$', views.events, name='events'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^courses/$', views.courses, name='courses'),
)
