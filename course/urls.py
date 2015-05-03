from django.conf.urls import patterns, url

from course import views

urlpatterns = patterns('',
    url(r'^search/(?P<termid>(\d+))/$', views.search_term, name='search by term'),
    url(r'^search/$', views.search, name='search'),
    url(r'^follow/add/$', views.follow_add, name='follow'),
    url(r'^follow/remove/$', views.follow_remove, name='unfollow'),
    url(r'^follow/has/$', views.follow_has, name='check follow'),
    url(r'^friends/$', views.find_friends, name='find facebook friends'),
    url(r'^course/(?P<term>(\d+))/(?P<crn>(\d+))/$', views.course, name='course'),
)
