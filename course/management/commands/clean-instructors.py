from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from course.models import Instructor, Course
from tabulate import tabulate

class Command(BaseCommand):
    help = 'Helps clean up duplicated instructors'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--duplicates', action='store_true')
        parser.add_argument('--stale', action='store_true')

    def handle(self, *args, **options):
        instructors = Instructor.objects.all()
        if options['duplicates']:
            self.stdout.write("Finding duplicates for {} instructors".format(len(instructors)))
            dupes = Instructor.objects.values('last_name').annotate(Count('id')).order_by().filter(id__count__gt=1)
            i = 1
            for item in dupes:
                self.stdout.write("Pair {}/{}".format(i, len(dupes)))
                instructors = Instructor.objects.filter(last_name=item['last_name'])
                table = []
                for instructor in instructors:
                    courses = Course.objects.filter(instructor=instructor)
                    table.append([len(table) + 1, instructor.last_name, instructor.first_name, len(courses), instructor.id])
                self.stdout.write(tabulate(table, headers=["#", "Last Name", "First Name", "Courses", "ID"], tablefmt="fancy_grid"))
                value = raw_input("Enter a value that should be migrated, or 0 to do nothing: ")
                if self.validate_index(value, table):
                    num = int(value)
                    migrate_from = instructors[num - 1]
                    if migrate_from:
                        value = raw_input("Enter a value that the instructor be migrated to: ")
                        if self.validate_index(value, table):
                            num = int(value)
                            migrate_to = instructors[num - 1]
                            courses = Course.objects.filter(instructor=migrate_from)
                            for course in courses:
                                course.instructor = migrate_to
                                course.save()
                            self.stdout.write("Migrated {} to {}".format(migrate_from, migrate_to))
                i += 1
        if options['stale']:
            table = []
            entries = []
            for instructor in instructors:
                courses = Course.objects.filter(instructor=instructor)
                if len(courses) == 0:
                    table.append([len(table) + 1, instructor.last_name, instructor.first_name, len(courses), instructor.id])
                    entries.append(instructor)
            self.stdout.write('Instructors which have no associated course:')
            self.stdout.write(tabulate(table, headers=["#", "Last Name", "First Name", "Courses", "ID"], tablefmt="fancy_grid"))
            if len(entries) > 0:
                value = raw_input("Delete all stale entries? (y/n): ")
                if value == "y" or value == "Y":
                    for entry in entries:
                        entry.delete()
                    self.stdout.write('{} entries deleted'.format(len(entries)))
        self.stdout.write('Done cleaning')

    def validate_index(self, value, table):
        if value.isdigit():
            num = int(value)
            if num == 0 or num > len(table) + 1:
                return False
            else:
                return True
        else:
            return False
