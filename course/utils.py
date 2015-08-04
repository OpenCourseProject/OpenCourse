from course.models import Course, FollowEntry
from schedule.models import ExamEntry
from django.db.models import Q

def exam_for_course(course):
    meeting_times = course.meeting_times.all()
    if len(meeting_times) == 0:
        return None

    meeting_time = meeting_times[0]
    start_time = meeting_time.start_time
    end_time = meeting_time.end_time
    days = meeting_time.days
    exams = ExamEntry.objects.filter(term=course.term, course_start_time=start_time, course_end_time=end_time)

    if days == "T" or days == "R":
        exams = exams.filter(Q(days=days) | Q(days="T/R"))
    elif days == "M" or days == "W":
        exams = exams.filter(Q(days=days) | Q(days="M/W") | Q(days="M/W/F"))
    else:
        exams = exams.filter(days=days)

    if len(exams) == 1:
        return exams[0]
    else:
        return None

def follow_get_course(follow):
    return Course.objects.get(term=follow.term, crn=follow.course_crn)

def follow_get_courses(follows):
    courses = []
    for follow in follows:
        courses.append(follow_get_course(follow))
    return courses
