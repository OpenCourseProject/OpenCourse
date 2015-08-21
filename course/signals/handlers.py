from django.dispatch import receiver
from django.db.models import signals
from course.models import Course, CourseVersion, FollowEntry
from course.utils import course_create_changelog
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from opencourse.models import EmailLog

@receiver(signals.post_save, sender=Course)
def version_course(sender, instance, **kwargs):
    CourseVersion.objects.create(instance).save()
    send_follow_email(instance)

def send_follow_email(course):
    term = course.term
    subject, from_email = 'Course Update: ' + course.title, 'admin@opencourseproject.com',
    course_link = 'https://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/'
    follow_link = 'https://opencourseproject.com/account/#follow'
    email_template_path = '/var/www/opencourseproject.com/opencourse/opencourse/static/assets/email/template.html'
    email_template = open(email_template_path).read()
    text_template_path = '/var/www/opencourseproject.com/opencourse/opencourse/static/assets/email/template.txt'
    text_template = open(text_template_path).read()
    detail_list = ''
    changes = course_create_changelog(course)
    for change in changes:
        detail_list = detail_list + '<li>' + change + '</li>'
    text_detail_list = ", ".join(changes)
    text_content = text_template.format(course=course.title, term=term.name, detail_list=text_detail_list, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link, follow_link=follow_link)
    html_content = email_template.format(course=course.title, term=term.name, detail_list=detail_list, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link, follow_link=follow_link)

    follows = FollowEntry.objects.filter(term=course.term, course_crn=course.crn)
    for follow in follows:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [follow.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Create a log
        EmailLog(user=follow.user, course=course, title=subject, content=text_content).save()
