from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from course.models import Term
from tastypie.models import ApiKey

class Profile(models.Model):
    user = models.OneToOneField(User)
    student_id = models.CharField(max_length=10, null=True)
    default_term = models.ForeignKey(Term, null=True)
    facebook_id = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.user.username

def create_user(sender, instance, created, **kwargs):
    # Create user profile if it doesn't exist
    try:
        Profile.objects.get(user=instance)
    except Profile.DoesNotExist:
        Profile(user=instance).save()
    # Create an API key if it doesn't exist
    try:
        ApiKey.objects.get(user=instance)
    except ApiKey.DoesNotExist:
        ApiKey.objects.create(user=instance)

signals.post_save.connect(create_user, sender=User)
