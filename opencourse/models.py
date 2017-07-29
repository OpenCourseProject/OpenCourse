from django.db import models
from course.models import Term, Course
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Report(models.Model):
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    description = models.TextField()
    responded = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Report by %s on %s' % (self.user, self.time_created.strftime("%m-%d-%y"))

class TermUpdate(models.Model):
    term = models.ForeignKey(Term)
    time_created = models.DateTimeField(auto_now_add=True)
    courses_parsed = models.IntegerField(default=0)
    courses_added = models.IntegerField(default=0)
    courses_updated = models.IntegerField(default=0)
    courses_deleted = models.IntegerField(default=0)
    time_completed = models.DateTimeField(null=True, blank=True)

    @property
    def is_completed(self):
        return self.time_completed != None

    def __unicode__(self):
        return 'Update for %s: %i new courses / %i' % (self.term, self.courses_added, self.courses_parsed)

class UpdateLog(models.Model):
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILED = 2
    STATUS_CHOICES = (
        (IN_PROGRESS, 'In Progress'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    )

    time_created = models.DateTimeField(auto_now_add=True)
    updates = models.ManyToManyField(TermUpdate)
    output = models.TextField(default="")
    time_completed = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=IN_PROGRESS, choices=STATUS_CHOICES)

    @property
    def courses_parsed(self):
        total = 0
        for update in self.updates.all():
            total += update.courses_parsed
        return total

    @property
    def courses_added(self):
        total = 0
        for update in self.updates.all():
            total += update.courses_added
        return total

    @property
    def courses_updated(self):
        total = 0
        for update in self.updates.all():
            total += update.courses_updated
        return total

    @property
    def is_completed(self):
        return self.status != 0

    def log(self, text):
        text = '{}: {}'.format(timezone.now().strftime('%H:%M:%S'),text)
        self.output += text + '\n'
        self.save()

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
        return self.enabled and (date.today() < self.expires) if self.expires else self.enabled

    def has_acknowledged(self, user):
        return user.id in self.acknowledged
