from django.dispatch import receiver
from django.db.models import signals
from opencourse.models import UpdateLog
from django.utils import timezone
from django.core.mail import mail_admins

@receiver(signals.pre_save, sender=UpdateLog)
def notify_failed_course_update(sender, instance, **kwargs):
    try:
        current = sender.objects.get(pk=instance.pk)
        if current.status == 0 and instance.status == 2:
            send_failure_email(instance)
    except sender.DoesNotExist:
        pass

def send_failure_email(log):
    message = "A course scrape failed at {time}. Here is the full output:\n\n{output}".format(time=timezone.now(), output=log.output)
    #mail_admins('Course scrape failed', message)
