from django.db import models
from django.contrib.auth.models import User
from course.models import Term

class Profile(models.Model):
    user = models.OneToOneField(User)
    learning_community = models.CharField(max_length=100, null=True, blank=True)
    default_term = models.ForeignKey(Term, null=True, blank=True)
    facebook_id = models.CharField(max_length=50, null=True, blank=True)
    preferred_name = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    orientation = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    show_archived_terms = models.BooleanField(default=False)
    show_colors_schedule = models.BooleanField(default=True)
    show_details_schedule = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username
