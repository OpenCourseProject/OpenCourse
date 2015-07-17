from course.models import Course

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
