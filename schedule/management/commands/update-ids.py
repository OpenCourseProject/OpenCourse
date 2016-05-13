from django.core.management.base import BaseCommand, CommandError
from schedule.models import ScheduleEntry

class Command(BaseCommand):

    def handle(self, *args, **options):
        entries = ScheduleEntry.objects.all()
        i = 0
        for entry in entries:
            i += 1
            entry.identifier = entry.generate_hash()
            entry.save()
            self.stdout.write('Updated entry {}/{}'.format(i, len(entries)))
        self.stdout.write('Successfully updated schedule identifiers')
