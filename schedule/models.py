from django.contrib.auth.models import User
from django.db import models
from course.models import Course, Term
import hashlib

class ScheduleEntry(models.Model):
    user = models.ForeignKey(User)
    term = models.ForeignKey(Term)
    course = models.ForeignKey(Course)
    identifier = models.CharField(max_length=100)

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"

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
        verbose_name = "exam"
        verbose_name_plural = "exams"

class ExamSource(models.Model):
    term = models.ForeignKey(Term)
    cnu_source = models.URLField()
    xl_source = models.URLField()
