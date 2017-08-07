from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
import json

class Term(models.Model):
    value = models.IntegerField(unique=True, primary_key=True, verbose_name ="Term Value")
    name = models.CharField(max_length=50, verbose_name="Term Name")
    priority = models.IntegerField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    update = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-priority', '-value']

class Instructor(models.Model):
    first_name = models.CharField(null=True, max_length=50, verbose_name="First Name")
    last_name = models.CharField(db_index=True, max_length=50, verbose_name="Last Name")
    email_address = models.EmailField(null=True, blank=True, default=None)
    rmp_link = models.URLField(null=True, blank=True, default=None, max_length=100, verbose_name="RateMyProfessor Link")
    position = models.CharField(null=True, blank=True, default=None, max_length=100, verbose_name="Position")
    no_update = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)

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

class Course(models.Model):
    OPEN = 1
    CLOSED = 0
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )
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
    status = models.IntegerField(verbose_name="Status", choices=STATUS_CHOICES)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

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

    @property
    def url(self):
        return "/course/{}/{}/".format(self.term.value, self.crn)

class CourseVersionManager(models.Manager):
    def create(self, course):
        data = serializers.serialize('json', [course])
        return CourseVersion(term=course.term, course_crn=course.crn, data=data)

    def find(self, course):
        return self.filter(term=course.term, course_crn=course.crn).order_by('-time_created')

class CourseVersion(models.Model):
    term = models.ForeignKey(Term)
    course_crn = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    objects = CourseVersionManager()

    def get_course(self):
        return Course.objects.get(term=self.term, crn=self.course_crn)

    def field_list(self):
        des = json.loads(self.data)
        return des[0]['fields']

    def __unicode__(self):
        return str(self.get_course()) + ' at ' + str(self.time_created)

class FollowEntry(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    course_crn = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'term', 'course_crn',)

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
    time_created = models.DateTimeField(auto_now_add=True)

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

class QueryLogManager(models.Manager):
    def create(self, user, term, data, result):
        data_json = json.dumps(data)
        return QueryLog(user=user, term=term, data=data_json, results=len(result))

class QueryLog(models.Model):
    user = models.ForeignKey(User, null=True)
    term = models.ForeignKey(Term)
    time_created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    results = models.IntegerField()
    objects = QueryLogManager()

    def field_list(self):
        return json.loads(self.data)

    def __unicode__(self):
        return str(self.user) + ' at ' + str(self.time_created)
