from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth.models import User
from tastypie.models import ApiKey
from account.models import Profile

@receiver(signals.post_save, sender=User)
def create_profile(sender, instance, **kwargs):
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
