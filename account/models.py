from django.db import models
from django.contrib.auth.models import User
from course.models import Term

class Profile(models.Model):
    user = models.OneToOneField(User)
    learning_community = models.CharField(max_length=100, null=True)
    default_term = models.ForeignKey(Term, null=True)
    facebook_id = models.CharField(max_length=50, null=True)
    preferred_name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.user.username
