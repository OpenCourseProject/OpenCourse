from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
    url(r'^$', views.account, name='account'),
    url(r'^link/facebook/$', views.link_facebook, name='link facebook'),
    url(r'^logout/$', views.logout, name='logout'),
)
