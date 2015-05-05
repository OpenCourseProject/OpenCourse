from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from course.models import Course, Term

class Command(BaseCommand):
    args = '<user_id term_id crn>'
    help = 'Emails a notification about a course status change'

    def handle(self, *args, **options):
        user = User.objects.get(id=int(args[0]))
        term = Term.objects.get(value=args[1])
        course = Course.objects.get(term=term, crn=int(args[2]))

        status = "CLOSED" if course.seats == 0 else "OPEN"

        subject, from_email, to = 'Course Update: ' + course.title, 'admin@opencourseproject.com', user.email
        text_content = course.title + ' for ' + term.name + ' is now ' + status + '. Click here to view the course page: http://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/'
        html_content = '<p><strong>' + course.title + '</strong> for ' + term.name + ' is now <strong>' + status + '</strong>.</p><p>Click here to view the course page: http://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
