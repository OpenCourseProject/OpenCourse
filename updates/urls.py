from django.conf.urls import patterns, url

from updates import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='updates'),
    url(r'^(?P<update>(\d+))/$', views.update, name='update'),
)
