from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from course.models import Term
from schedule.models import ExamEntry
from tabulate import tabulate

class Command(BaseCommand):
    help = 'Helps clean up duplicated exam periods'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--duplicates', action='store_true')

    def handle(self, *args, **options):
        terms = Term.objects.all()
        if options['duplicates']:
            self.stdout.write("Finding duplicated exams for {} terms".format(len(terms)))
            for term in terms:
                exams = ExamEntry.objects.filter(term=term)
                seen = []
                dupes = []
                for exam in exams:
                    for value in seen:
                        if value.days == exam.days and value.course_start_time == exam.course_start_time and value.course_end_time == exam.course_end_time:
                            dupes.append(exam)
                    seen.append(exam)
                if len(dupes) > 0:
                    self.stdout.write("-- {}".format(term))
                    for dupe in dupes:
                        ii = exams.filter(days=dupe.days, course_start_time=dupe.course_start_time, course_end_time=dupe.course_end_time)
                        ii[1].delete()
                        self.stdout.write("{}".format(ii))
        self.stdout.write('Done cleaning')
