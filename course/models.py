from django.db import models
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Q
import json

class Term(models.Model):
    value = models.IntegerField(unique=True, primary_key=True, verbose_name ="Term Value")
    name = models.CharField(max_length=50, verbose_name="Term Name")

    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    first_name = models.CharField(null=True, max_length=50, verbose_name="First Name")
    last_name = models.CharField(db_index=True, max_length=50, verbose_name="Last Name")
    rmp_score = models.DecimalField(null=True, decimal_places=1, max_digits=2, verbose_name="RateMyProfessor Score")
    rmp_link = models.URLField(max_length=100, null=True, verbose_name="RateMyProfessor Link")

    def __unicode__(self):
        name = self.last_name
        if self.first_name and len(self.first_name) > 0:
            name += ", " + self.first_name
        if self.rmp_score:
            name += " (" + str(self.rmp_score) + ")"
        return name

    @property
    def full_name(self):
        return first_name + " " + last_name

class Course(models.Model):
    term = models.ForeignKey(Term)
    crn = models.IntegerField(db_index=True, verbose_name="CRN")
    course = models.CharField(db_index=True, max_length=50, verbose_name="Course")
    course_link = models.URLField(max_length=200, verbose_name="Course Link")
    section = models.CharField(max_length=5, verbose_name="Section")
    title = models.CharField(max_length=50, verbose_name="Title")
    bookstore_link = models.URLField(max_length=200, verbose_name="Bookstore Link")
    hours = models.CharField(max_length=5, verbose_name="Hours")
    llc = models.CharField(max_length=10, verbose_name="LLC/AoI")
    ctype = models.CharField(max_length=10, verbose_name="Type")
    days = models.CharField(db_index=True, max_length=50, verbose_name="Days")
    start_time = models.TimeField(db_index=True, null=True, verbose_name="Start")
    end_time = models.TimeField(db_index=True, null=True, verbose_name="End")
    location = models.CharField(max_length=20, verbose_name="Location")
    instructor = models.ForeignKey(Instructor, verbose_name="Instructor")
    seats = models.IntegerField(db_index=True, verbose_name="Seats Left")
    status = models.IntegerField(verbose_name="Status")

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

    def __unicode__(self):
        return "%s: %s" % (self.course, self.title)

    def to_json(self):
       data = json.dumps(self, default=lambda o: o.__dict__,)
       parse = json.loads(data)
       parse['type'] = parse['ctype']
       del parse['ctype']
       del parse['_state']
       return json.dumps(parse, sort_keys=True, indent=4)

class FollowEntry(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    course = models.ForeignKey(Course)
