from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
