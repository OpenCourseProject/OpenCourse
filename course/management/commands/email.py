from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from course.models import Course, Term

class Command(BaseCommand):
    args = '<user_id term_id crn>'
    help = 'Emails a notification about a course status change'

    def handle(self, *args, **options):
        email_template_path = '/var/www/opencourseproject.com/opencourse/opencourse/static/assets/email/template.html'
        email_template = open(email_template_path).read()
        text_template_path = '/var/www/opencourseproject.com/opencourse/opencourse/static/assets/email/template.txt'
        text_template = open(text_template_path).read()
        user = User.objects.get(id=int(args[0]))
        term = Term.objects.get(value=args[1])
        course = Course.objects.get(term=term, crn=int(args[2]))

        course_link = 'https://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/'
        description = 'There {} now {} {} left for this class.'.format(('is' if course.seats == 1 else 'are'), course.seats, ('seat' if course.seats == 1 else 'seats'))
        status = "CLOSED" if course.seats == 0 else "OPEN"

        subject, from_email, to = 'Course Update: ' + course.title, 'admin@opencourseproject.com', user.email
        text_content = text_template.format(course=course.title, term=term.name, status=status, description=description, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link)
        html_content = email_template.format(course=course.title, term=term.name, status=status, description=description, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
