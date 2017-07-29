from course.models import Course, CourseVersion, Instructor, FollowEntry, MeetingTime
from schedule.models import ExamEntry
from django.db.models import Q
from django.utils.safestring import SafeString

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

def create_changelog(old_version, new_version, plaintext=False):
    changes = []
    for field, value in new_version.field_list().iteritems():
        try:
            old_value = old_version.field_list()[field]
        except:
            if field == 'deleted':
                old_value = False
        new_value = value
        if old_value != new_value:
            if field == 'status':
                old_value = dict(Course._meta.get_field('status').choices)[old_value]
                new_value = dict(Course._meta.get_field('status').choices)[new_value]
            if field == 'meeting_times':
                old_value = ", ".join([str(i) for i in MeetingTime.objects.filter(id__in=old_value)])
                new_value = ", ".join([str(i) for i in MeetingTime.objects.filter(id__in=new_value)])
            if field == 'instructor':
                try:
                    old_value = Instructor.objects.get(id=old_value)
                except Instructor.DoesNotExist:
                    old_value = None
                try:
                    new_value = Instructor.objects.get(id=new_value)
                except Instructor.DoesNotExist:
                    new_value = None
            verbose_name = Course._meta.get_field_by_name(field)[0].verbose_name
            if old_value == '':
                old_value = 'none'
            if new_value == '':
                new_value = 'none'
            string = verbose_name + ' changed from ' + str(old_value) +  ' to ' + str(new_value) if plaintext else SafeString(verbose_name + ' changed from <strong>' + str(old_value) +  '</strong> to <strong>' + str(new_value) + '</strong>')
            if field == 'deleted':
                if new_value:
                    string = 'Course was removed from the Schedule of Classes by the registrar' if plaintext else SafeString('Course was <strong>removed</strong> from the Schedule of Classes by the registrar')
                else:
                    string = 'Course was re-added to the Schedule of Classes by the registrar' if plaintext else SafeString('Course was <strong>re-added</strong> to the Schedule of Classes by the registrar')
            changes.append(string)
    return changes

def course_create_changelog(course):
    version_list = CourseVersion.objects.find(course)
    if len(version_list) > 1:
        new_version = version_list[0]
        old_version = version_list[1]
        return create_changelog(old_version, new_version)
    else:
        return []
