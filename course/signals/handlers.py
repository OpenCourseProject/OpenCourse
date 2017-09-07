from django.dispatch import receiver
from django.db.models import signals
from course.models import Course, CourseVersion, FollowEntry
from course.utils import course_create_changelog
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.conf import settings
from opencourse.models import EmailLog

@receiver(signals.post_save, sender=Course)
def version_course(sender, instance, **kwargs):
    CourseVersion.objects.create(instance).save()
    send_follow_email(instance)

def send_follow_email(course):
    if settings.DEBUG or settings.TESTING:
        return

    term = course.term
    subject, from_email = 'Course Update: ' + course.title, 'admin@opencourseproject.com',
    course_link = 'https://opencourseproject.com/course/' + str(term.value) + '/' + str(course.crn) + '/'
    follow_link = 'https://opencourseproject.com/account/#follow'
    email_template_path = settings.STATIC_ROOT + '/assets/email/template.html'
    email_template = open(email_template_path).read()
    text_template_path = settings.STATIC_ROOT + '/assets/email/template.txt'
    text_template = open(text_template_path).read()
    detail_list = ''
    if course.deleted:
        detail_list = """
        <p>
        This course has been <strong>REMOVED from the Schedule of Classes</strong>.
        Courses are occasionally removed by the registrar early in the scheduling process as changes
        are made to instructor availability and changes in department scheduling.
        </p>
        <p>
        You will no longer be able to enroll in this section, and if you are planning to take this
        class you should search for <a href="https://opencourseproject.com/search/?term={term}&course={course}">a different {course} section</a> that is still available.
        </p>""".format(term=course.term.value, course=course.course)
        text_detail_list = """
        This course has been REMOVED from the Schedule of Classes.
        Courses are occasionally removed by the registrar early in the scheduling process as changes
        are made to instructor availability and changes in department scheduling.
        You will no longer be able to enroll in this section, and if you are planning to take this
        class you should search for a different {course} section that is still available.""".format(course=course.course)
        subject = 'Course no longer available: ' + course.title
    else:
        changes = course_create_changelog(course)
        for change in changes:
            detail_list = detail_list + '<li>' + change + '</li>'
        text_detail_list = ", ".join(changes)
        if len(changes) == 0 or len(detail_list) == 0:
            return
    text_content = text_template.format(course=course.title, term=term.name, detail_list=text_detail_list, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link, follow_link=follow_link)
    html_content = email_template.format(course=course.title, term=term.name, detail_list=detail_list, course_crn=course.crn, course_section=course.section, course_instructor=str(course.instructor), course_link=course_link, follow_link=follow_link)

    follows = FollowEntry.objects.filter(term=course.term, course_crn=course.crn)
    for follow in follows:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [follow.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Create a log
        EmailLog(user=follow.user, course=course, title=subject, content=text_content).save()
