from course.models import Course, FollowEntry
from schedule.models import ExamEntry
from django.db.models import Q

def exam_for_course(course):
    exams = ExamEntry.objects.filter(term=course.term, course_start_time=course.start_time, course_end_time=course.end_time)

    if course.days == "T" or course.days == "R":
        exams = exams.filter(Q(days=course.days) | Q(days="T/R"))
    elif course.days == "M" or course.days == "W":
        exams = exams.filter(Q(days=course.days) | Q(days="M/W") | Q(days="M/W/F"))
    else:
        exams = exams.filter(days=course.days)

    if len(exams) == 1:
        return exams[0]
    else:
        return None
