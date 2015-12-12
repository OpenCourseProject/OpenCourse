from course.models import Course

COLORS = [
    '#2ecc71',
    '#3498db',
    '#e67e22',
    '#1dd2af',
    '#e74c3c',
    '#19b5fe',
    '#34495e',
    '#7f8c8d',
    '#9b59b6',
    '#bdc3c7',
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
