from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Q
import json
import reversion

class Term(models.Model):
    value = models.IntegerField(unique=True, primary_key=True, verbose_name ="Term Value")
    name = models.CharField(max_length=50, verbose_name="Term Name")

    def __unicode__(self):
        return self.name

@reversion.register
class Instructor(models.Model):
    first_name = models.CharField(null=True, max_length=50, verbose_name="First Name")
    last_name = models.CharField(db_index=True, max_length=50, verbose_name="Last Name")
    email_address = models.EmailField(null=True, blank=True, default=None)
    rmp_score = models.DecimalField(null=True, blank=True, default=None, decimal_places=1, max_digits=2, verbose_name="Rating")
    rmp_link = models.URLField(null=True, blank=True, default=None, max_length=100, verbose_name="RateMyProfessor Link")
    position = models.CharField(null=True, blank=True, default=None, max_length=100, verbose_name="Position")
    no_update = models.BooleanField(default=False)

    def __unicode__(self):
        name = self.last_name
        if self.first_name and len(self.first_name) > 0:
            name += ", " + self.first_name
        return name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

class Attribute(models.Model):
    value = models.CharField(max_length=10, verbose_name="Attribute Value")
    name = models.CharField(max_length=50, verbose_name="Attribute Name")

    def __unicode__(self):
        return self.name

class MeetingTime(models.Model):
    days = models.CharField(db_index=True, max_length=50, verbose_name="Days")
    start_time = models.TimeField(db_index=True, null=True, verbose_name="Start")
    end_time = models.TimeField(db_index=True, null=True, verbose_name="End")

    def __unicode__(self):
        return "%s, %s - %s" % (self.days, self.start_time.strftime('%I:%M %p'), self.end_time.strftime('%I:%M %p'))

@reversion.register
class Course(models.Model):
    term = models.ForeignKey(Term)
    crn = models.IntegerField(db_index=True, verbose_name="CRN")
    course = models.CharField(db_index=True, max_length=50, verbose_name="Course")
    course_link = models.URLField(max_length=200, verbose_name="Course Link")
    section = models.CharField(max_length=5, verbose_name="Section")
    title = models.CharField(max_length=50, verbose_name="Title")
    bookstore_link = models.URLField(max_length=200, verbose_name="Bookstore Link")
    hours = models.CharField(max_length=5, verbose_name="Hours")
    attributes = models.CharField(max_length=10, verbose_name="Attributes", null=True, blank=True)
    ctype = models.CharField(max_length=10, verbose_name="Type")
    meeting_times = models.ManyToManyField(MeetingTime, blank=True, verbose_name="Meeting Time")
    location = models.CharField(max_length=20, null=True, blank=True, verbose_name="Location")
    instructor = models.ForeignKey(Instructor, null=True, blank=True, verbose_name="Instructor")
    seats = models.IntegerField(db_index=True, verbose_name="Seats Left")
    status = models.IntegerField(verbose_name="Status")

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __unicode__(self):
        return "%s: %s" % (self.course, self.title)

    @property
    def get_attributes(self):
        attr = []
        for value in self.attributes.split('  '):
            attr.append(Attribute.objects.get(value=value).name)
        return ", ".join(attr)

    @property
    def primary_meeting_time(self):
        times = self.meeting_times.all()
        if len(times) > 0:
            return times[0]
        else:
            return None

    @property
    def secondary_meeting_times(self):
        times = self.meeting_times.all()
        if len(times) > 1:
            return times[1:]
        else:
            return None

class FollowEntry(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    course_crn = models.IntegerField()

    def __unicode__(self):
        return "%s: %d" % (self.user, self.course_crn)

class Material(models.Model):
    term = models.ForeignKey(Term)
    course_crn = models.IntegerField()
    isbn = models.BigIntegerField(null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    edition = models.CharField(max_length=20)
    year = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title

class InstructorSuggestion(models.Model):
    instructor = models.ForeignKey(Instructor)
    user = models.ForeignKey(User)
    time_created = models.DateTimeField(auto_now_add=True)
    email_address = models.EmailField(blank=True, null=True)
    rmp_link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return str(self.instructor)
