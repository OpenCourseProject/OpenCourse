from django.dispatch import receiver
from django.db.models import signals
from schedule.models import ScheduleEntry, ScheduleTransaction

@receiver(signals.post_save, sender=ScheduleEntry)
def create_add_transaction(sender, instance, **kwargs):
    ScheduleTransaction(user=instance.user, term=instance.term, course_crn=instance.course_crn, action="ADD").save()
    pass

@receiver(signals.pre_delete, sender=ScheduleEntry)
def create_drop_transaction(sender, instance, **kwargs):
    ScheduleTransaction(user=instance.user, term=instance.term, course_crn=instance.course_crn, action="DROP").save()
    pass
