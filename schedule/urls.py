from django.conf.urls import patterns, url

from schedule import views
from schedule.models import ScheduleEntry
from django.db.models import signals
from schedule.signals import handlers

urlpatterns = patterns('',
    url(r'^$', views.schedule, name='schedule'),
    url(r'^exam/(?P<termid>(\d+))/$', views.exam_schedule, name='exam schedule'),
    url(r'^calendar/course/$', views.schedule_calendar, name='schedule calendar events'),
    url(r'^calendar/exam/$', views.exam_calendar, name='exam calendar events'),
    url(r'^(?P<identifier>(\w+))/$', views.schedule_view, name='view schedule'),
)

# Signal connections
signals.post_save.connect(handlers.create_add_transaction, sender=ScheduleEntry)
signals.pre_delete.connect(handlers.create_drop_transaction, sender=ScheduleEntry)
