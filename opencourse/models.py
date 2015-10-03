from django.db import models
from course.models import Course
from django.contrib.auth.models import User
from datetime import date

class Report(models.Model):
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    description = models.TextField()
    responded = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Report by %s on %s' % (self.user, self.time_created.strftime("%m-%d-%y"))

class CourseUpdateLog(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    courses_parsed = models.IntegerField()
    courses_added = models.IntegerField()
    courses_updated = models.IntegerField()

    def __unicode__(self):
        return 'Update at %s: %i new courses / %i' % (self.time_created.strftime("%m-%d-%y"), self.courses_added, self.courses_parsed)

class EmailLog(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return 'Email to %s on %s for %s' % (self.user, self.time_created.strftime("%m-%d-%y"), self.course)

class Alert(models.Model):
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'
    STYLE_CHOICES = (
        (SUCCESS, 'Success'),
        (INFO, 'Info'),
        (WARNING, 'Warning'),
        (DANGER, 'Danger'),
    )

    time_created = models.DateTimeField(auto_now_add=True)
    style = models.CharField(max_length=10, choices=STYLE_CHOICES)
    message = models.CharField(max_length=1000)
    enabled = models.BooleanField(default=False)
    expires = models.DateTimeField(null=True, blank=True)
    acknowledged = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return 'Alert: %s'.format(self.message)

    @property
    def is_active(self):
        return self.enabled and (date.today() < self.expires) if self.expires else True

    def has_acknowledged(self, user):
        return user.id in self.acknowledged
