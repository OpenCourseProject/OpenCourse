from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from course.models import Term

class Profile(models.Model):
    user = models.OneToOneField(User)
    student_id = models.CharField(max_length=10, null=True)
    default_term = models.ForeignKey(Term, null=True)
    facebook_id = models.CharField(max_length=50, null=True)

def create_profile(sender, instance, created, **kwargs):
    profile = Profile.objects.get(user=instance)
    if not profile:
        Profile(user=instance).save()

signals.post_save.connect(create_profile, sender=User)
