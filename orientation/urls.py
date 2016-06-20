from django.conf.urls import patterns, url

from orientation import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^majors/$', views.majors, name='majors'),
)
