from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max, Count
from account.models import Profile
from course.models import Course, FollowEntry
from schedule.models import ScheduleEntry
from tabulate import tabulate

class Command(BaseCommand):
    help = 'Helps clean up duplicated schedule entries'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--schedule', action='store_true')
        parser.add_argument('--follow', action='store_true')

    def handle(self, *args, **options):
        table = []
        if options['schedule']:
            unique_fields = ['user', 'term', 'course_crn']
            dupes = (ScheduleEntry.objects.values(*unique_fields)
                                         .order_by()
                                         .annotate(max_id=Max('id'),
                                                   count_id=Count('id'))
                                         .filter(count_id__gt=1))

            entries = []
            for dupe in dupes:
                entry = ScheduleEntry.objects.filter(**{x: dupe[x] for x in unique_fields}).exclude(id=dupe['max_id'])
                entries.append(entry)
                table.append([len(table) + 1, entry[0].user.username, len(entry), entry[0].course_crn])
            self.stdout.write('Duplicated schedule entries:')
            self.stdout.write(tabulate(table, headers=["#", "Username", "Count", "Course CRN"], tablefmt="fancy_grid"))
            if len(entries) > 0:
                value = raw_input("Delete all duplicates? (y/n): ")
                if value == "y" or value == "Y":
                    for entry in entries:
                        entry.delete()
                    self.stdout.write('{} duplicates deleted'.format(len(entries)))
        if options['follow']:
            unique_fields = ['user', 'term', 'course_crn']
            dupes = (FollowEntry.objects.values(*unique_fields)
                                         .order_by()
                                         .annotate(max_id=Max('id'),
                                                   count_id=Count('id'))
                                         .filter(count_id__gt=1))

            entries = []
            for dupe in dupes:
                entry = FollowEntry.objects.filter(**{x: dupe[x] for x in unique_fields}).exclude(id=dupe['max_id'])
                entries.delete(entry)
                table.append([len(table) + 1, entry[0].user.username, len(entry), entry[0].course_crn])
            self.stdout.write('Duplicated follow entries:')
            self.stdout.write(tabulate(table, headers=["#", "Username", "Count", "Course CRN"], tablefmt="fancy_grid"))
            if len(entries) > 0:
                value = raw_input("Delete all duplicates? (y/n): ")
                if value == "y" or value == "Y":
                    for entry in entries:
                        entry.delete()
                    self.stdout.write('{} duplicates deleted'.format(len(entries)))
        self.stdout.write('Done cleaning')
