from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from course.models import Term, Instructor, Attribute, MeetingTime, Course, CourseVersion, QueryLog, InstructorSuggestion
from course.utils import create_changelog
from datetime import time
from lxml import html

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

    def test_data(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        versions = CourseVersion.objects.find(course)
        version = versions[len(versions) - 1]
        for value in version.field_list():
            attr1 = getattr(course, value)
            attr2 = version.field_list()[value]
            if value == 'term':
                attr1 = attr1.value
            if value == 'instructor':
                attr1 = attr1.id
            if value == 'meeting_times':
                attr1 = [i.id for i in attr1.all()]
            self.assertEqual(attr1, attr2)

    def test_changelog(self):
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        course.status = 0
        course.save()
        instructor = Instructor.objects.create(first_name="Bill", last_name="Gates", rmp_score=1.0, rmp_link="http://microsoft.com")
        course.instructor = instructor
        course.save()
        versions = CourseVersion.objects.find(course)
        changes = create_changelog(versions[0], versions[len(versions) - 1], True)
        self.assertEqual(3, len(changes))
        expected = [
            'Status changed from Open to Closed',
            'Instructor changed from Instructor, Joe to Gates, Bill',
            'Meeting Time changed from none to MW, 10:00 AM - 11:15 AM, F, 10:00 AM - 10:50 AM'
        ]
        self.assertEqual(expected, changes)

class WebSearchTestCase(TestCase):
    def setUp(self):
        create_dummy_course()
        user = User.objects.create_user('ironman', 'ironman@gmail.com', 'imironman123')

    def test_search(self):
        c = Client()
        response = c.get('/search/', secure=True)
        self.assertEqual(200, response.status_code)

    def test_search_by_term(self):
        c = Client()
        term = Term.objects.get(value=42)
        data = {
            'term': term.value
        }
        response = c.get('/search/', {'term': term.value}, secure=True)
        self.assertEqual(200, response.status_code)

    def test_search_by_course(self):
        c = Client()
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        data = {
            'term': term.value,
            'crn': course.crn,
        }
        response = c.post('/search/', data, secure=True)
        self.assertEqual(200, response.status_code)
        page = html.fromstring(response.content)
        course_list = page.xpath(".//tbody/tr")
        self.assertEqual(1, len(course_list))

    def test_search_property(self):
        c = Client()
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        values = [
            {'course': course.course},
            {'days': course.primary_meeting_time.days},
            {'start_hour': '10', 'start_minute': '00', 'start_meridiem': 'a.m.'},
            {'end_hour': '11', 'end_minute': '15', 'end_meridiem': 'a.m.'},
            {'instructor': course.instructor.last_name},
            {'min_rating': course.instructor.rmp_score},
        ]
        for data in values:
            data['term'] = str(term.value)
            response = c.post('/search/', data, secure=True)
            self.assertEqual(200, response.status_code)
            page = html.fromstring(response.content)
            course_list = page.xpath(".//tbody/tr")
            self.assertEqual(1, len(course_list))

    def test_search_logs(self):
        c = Client()
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        data = {
            'term': term.value,
            'crn': course.crn,
        }
        response = c.post('/search/', data, secure=True)
        self.assertEqual(200, response.status_code)
        logs = QueryLog.objects.all()
        self.assertEqual(1, len(logs))
        self.assertEqual(str(course.crn), logs[0].field_list()['crn'])

    def test_course_page(self):
        c = Client()
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        response = c.get('/course/' + str(term.value) + '/' + str(course.crn) + '/', secure=True)
        self.assertEqual(200, response.status_code)
        page = html.fromstring(response.content)
        details = page.xpath(".//ul[@class='list-group']/li/p/text()")
        self.assertEqual(term.name, details[0])
        self.assertEqual(str(course.crn), details[1])

    def test_instructor_suggestion_unauthorized(self):
        c = Client()
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        data = {
            'email_address': 'joe.instructor@cnu.edu',
            'rmp_link': 'http://ratemyprofessors.com/'
        }
        response = c.post('/course/' + str(term.value) + '/' + str(course.crn) + '/', data, secure=True)
        suggestions = InstructorSuggestion.objects.all()
        self.assertEqual(0, len(suggestions))
        self.assertEqual('Unauthorized', response.content)

    def test_instructor_suggestion(self):
        c = Client()
        c.login(username='ironman', password='imironman123')
        term = Term.objects.get(value=42)
        course = Course.objects.get(term=term, crn=1234)
        data = {
            'email_address': 'joe.instructor@cnu.edu',
            'rmp_link': 'http://ratemyprofessors.com/'
        }
        response = c.post('/course/' + str(term.value) + '/' + str(course.crn) + '/', data, secure=True)
        self.assertEqual(200, response.status_code)
        suggestions = InstructorSuggestion.objects.all()
        self.assertEqual(1, len(suggestions))
        self.assertEqual(course.instructor, suggestions[0].instructor)
        self.assertEqual('joe.instructor@cnu.edu', suggestions[0].email_address)
        self.assertEqual('http://ratemyprofessors.com/', suggestions[0].rmp_link)

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
