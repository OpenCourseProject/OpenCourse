from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^username/$', views.api_username, name='get api username'),
    url(r'^key/$', views.api_key, name='get api key'),
)
