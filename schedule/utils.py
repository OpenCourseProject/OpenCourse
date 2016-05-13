from course.models import Term, Course
from django.contrib.auth.models import User
import hashlib

COLORS = [
    'rgba(46, 204, 113, 0.8)',
    'rgba(26, 188, 156, 0.8)',
    'rgba(230, 126, 34, 0.8)',
    'rgba(52, 152, 219, 0.8)',
    'rgba(52, 73, 94, 0.8)',
    'rgba(231, 76, 60, 0.8)',
    'rgba(155, 89, 182, 0.8)',
    'rgba(127, 140, 141, 0.8)',
    'rgba(230, 126, 34, 0.8)',
]

def schedule_get_course(entry):
    try:
        return Course.objects.get(term=entry.term, crn=entry.course_crn)
    except Course.DoesNotExist:
        return None

def schedule_get_courses(entries):
    courses = []
    for entry in entries:
        courses.append(schedule_get_course(entry))
    return courses

def get_colors_for_courses(courses):
    values = {}
    for i in range(0, len(courses)):
        course = courses[i]
        color = COLORS[i % len(COLORS)]
        values[course] = color
    return values

def get_identifier(user, term):
    hash = hashlib.md5(b'{}:{}:{}'.format(user.username, user.date_joined, term.name))
    return hash.hexdigest()[:15]
