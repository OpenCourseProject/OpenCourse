from django.conf.urls import patterns, url

from schedule import views

urlpatterns = patterns('',
    url(r'^$', views.schedule, name='schedule'),
    url(r'^add/$', views.schedule_add, name='add to schedule'),
    url(r'^remove/$', views.schedule_remove, name='remove from schedule'),
    url(r'^has/$', views.schedule_has, name='check schedule'),
    url(r'^(?P<termid>(\d+))/$', views.schedule_term, name='view schedule by term'),
    url(r'^(?P<identifier>(\w+))/$', views.schedule_view, name='view schedule'),
)
