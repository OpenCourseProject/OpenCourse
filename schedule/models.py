from django.contrib.auth.models import User
from django.db import models
from course.models import Course, Term
import hashlib

class ScheduleEntry(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    course_crn = models.IntegerField()
    identifier = models.CharField(max_length=100)

    class Meta:
        verbose_name = "scheduled course"
        verbose_name_plural = "scheduled courses"

    def __unicode__(self):
        return "%s: %d" % (self.user, self.course_crn)

    def generate_hash(self):
        hash = hashlib.md5(b'%s:%s' % (str(self.user.username), str(self.term.name)))
        return hash.hexdigest()[:15]

    def save(self, *args, **kwargs):
        self.identifier = self.generate_hash()
        super(ScheduleEntry, self).save(*args, **kwargs)

class ExamEntry(models.Model):
    term = models.ForeignKey(Term)
    days = models.CharField(db_index=True, max_length=50)
    course_start_time = models.TimeField(db_index=True)
    course_end_time = models.TimeField(db_index=True)
    exam_date = models.DateField()
    exam_start_time = models.TimeField()
    exam_end_time = models.TimeField()

    class Meta:
        verbose_name = "exam period"
        verbose_name_plural = "exam periods"

    def __unicode__(self):
        return "%s: %s %s-%s" % (self.term.name, self.days, self.course_start_time, self.course_end_time)

class ExamSource(models.Model):
    term = models.ForeignKey(Term)
    cnu_source = models.URLField()
    xl_source = models.URLField()

    def __unicode__(self):
        return self.term.name
