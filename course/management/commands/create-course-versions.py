from django.core.management.base import BaseCommand, CommandError
from course.models import Course, CourseVersion

class Command(BaseCommand):
    help = 'Creates intial course versions'

    def handle(self, *args, **options):
        courses = Course.objects.all()
        self.stdout.write('Creating intial versions for ' + str(len(courses)) + ' courses')
        for course in courses:
            CourseVersion.objects.create(course).save()
        self.stdout.write('Intial versions created')
