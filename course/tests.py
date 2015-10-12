from django.test import TestCase
from course.models import Term, Instructor, Attribute, MeetingTime, Course, CourseVersion
from datetime import time

class TermTestCase(TestCase):
    def setUp(self):
        Term.objects.create(value=42, name="The Answer")

    def test_term_named_correctly(self):
        term = Term.objects.get(value=42)
        self.assertEqual(str(term), term.name)

class InstructorTestCase(TestCase):
    def setUp(self):
        Instructor.objects.create(first_name="Joe", last_name="Instructor", rmp_score=5.0, rmp_link="http://google.com")

    def test_instructor_named_correctly(self):
        instructor = Instructor.objects.get(last_name="Instructor")
        self.assertEqual(str(instructor), "Instructor, Joe")

    def test_instructor_full_name(self):
        instructor = Instructor.objects.get(last_name="Instructor")
        self.assertEqual(instructor.full_name, "Joe Instructor")

    def test_instructor_update(self):
        instructor = Instructor.objects.get(last_name="Instructor")
        self.assertEqual(instructor.no_update, False)

class AttributeTestCase(TestCase):
    def setUp(self):
        Attribute.objects.create(value="ABCD", name="Alphabet Literacy")

    def test_attribute_named_correctly(self):
        attr = Attribute.objects.get(value="ABCD")
        self.assertEqual(str(attr), attr.name)

class CourseTestCase(TestCase):
    def setUp(self):
        create_dummy_course()
        Attribute.objects.create(value="ABCD", name="Alphabet Literacy")
        Attribute.objects.create(value="SI", name="Swimming Intensive")

    def test_course_named_correctly(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        self.assertEqual(str(course), "ALPH 101: Understanding the Alphabet")

    def test_course_version(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        versions = CourseVersion.objects.find(course)
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0].get_course(), course)

    def test_attributes(self):
        attr1 = Attribute.objects.get(value="ABCD")
        attr2 = Attribute.objects.get(value="SI")
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        attributes = course.get_attributes
        self.assertEqual(attributes, ", ".join([attr1.name, attr2.name]))

    def test_meeting_times(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        primary_time = course.primary_meeting_time
        secondary_times = course.secondary_meeting_times
        self.assertEqual("MW", primary_time.days)
        self.assertEqual(1, len(secondary_times))
        self.assertEqual("F", secondary_times[0].days)

    def test_meeting_times_search(self):
        start_time = time(10, 00)
        courses = Course.objects.filter(meeting_times__start_time=start_time).distinct()
        self.assertEqual(1, len(courses))
        end_time = time(10, 50)
        courses = Course.objects.filter(meeting_times__days="F", meeting_times__end_time=end_time).distinct()
        self.assertEqual(1, len(courses))

class VersioningTestCase(TestCase):
    def setUp(self):
        create_dummy_course()

    def test_versioning_change(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        course.location = "MARS 101"
        course.save()
        versions = CourseVersion.objects.find(course)
        self.assertEqual(3, len(versions))
        version = versions[0]
        self.assertEqual("ROOM 217", version.field_list()['location'])
        self.assertEqual([], version.field_list()['meeting_times'])
        version = versions[1]
        self.assertEqual("ROOM 217", version.field_list()['location'])
        self.assertEqual([i.id for i in course.meeting_times.all()], version.field_list()['meeting_times'])
        version = versions[2]
        self.assertEqual("MARS 101", version.field_list()['location'])

def create_dummy_course():
        term = Term.objects.create(value=42, name="The Answer")
        crn = 1234
        course = "ALPH 101"
        course_link = "http://google.com"
        section = "1"
        title = "Understanding the Alphabet"
        bookstore_link = "http://google.com"
        hours = "3"
        attributes = "ABCD  SI"
        ctype = "Lec"
        location = "ROOM 217"
        instructor = Instructor.objects.create(first_name="Joe", last_name="Instructor", rmp_score=6.0, rmp_link="http://google.com")
        seats = 1
        status = 1
        course = Course.objects.create(term=term, crn=crn, course=course, course_link=course_link, section=section, title=title, bookstore_link=bookstore_link, hours=hours, attributes=attributes, ctype=ctype, location=location, instructor=instructor, seats=seats, status=status)
        start_time = time(10, 00)
        end_time = time(11, 15)
        meeting_times = []
        meeting_times.append(MeetingTime.objects.create(days="MW", start_time=start_time, end_time=end_time))
        end_time = time(10, 50)
        meeting_times.append(MeetingTime.objects.create(days="F", start_time=start_time, end_time=end_time))
        course.meeting_times = meeting_times
        course.save()
        return course
