from course.models import Course, FollowEntry, MeetingTime
from schedule.models import ExamEntry
from django.db.models import Q
from django.utils.safestring import SafeString
import reversion

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

def create_changelog(old_version, new_version):
    changes = []
    for field, value in new_version.field_dict.iteritems():
        old_value = old_version.field_dict[field]
        new_value = value
        if old_value != new_value:
            if field == 'status':
                old_value = 'OPEN' if old_value == 1 else 'CLOSED'
                new_value = 'OPEN' if new_value == 1 else 'CLOSED'
            if field == 'meeting_times':
                old_value = ", ".join([str(i) for i in MeetingTime.objects.filter(id__in=old_value)])
                new_value = ", ".join([str(i) for i in MeetingTime.objects.filter(id__in=new_value)])
                pass
            field_name = Course._meta.get_field_by_name(field)[0].verbose_name
            changes.append(SafeString(field_name + ' changed from <strong>' + str(old_value) +  '</strong> to <strong>' + str(new_value) + '</strong>'))
    return changes

def course_create_changelog(course):
    version_list = reversion.get_for_object(course)
    if len(version_list) > 1:
        new_version = version_list[0]
        old_version = version_list[1]
        return create_changelog(old_version, new_version)
    else:
        return []
