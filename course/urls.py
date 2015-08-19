from django.conf.urls import patterns, url

from course import views
from django.db.models import signals
from course.signals import handlers
from reversion.models import Version

urlpatterns = patterns('',
    url(r'^search/$', views.search, name='search'),
    url(r'^friends/$', views.find_friends, name='find facebook friends'),
    url(r'^course/(?P<term>(\d+))/(?P<crn>(\d+))/$', views.course, name='course'),
)

# Signal connections
signals.post_save.connect(handlers.send_follow_email, sender=Version)
