from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from course.models import Term, Course
from opencourse.models import Report, UpdateLog
from django.core.management import call_command
from django.conf import settings

class ReportTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('ironman', 'ironman@gmail.com', 'imironman123')

    def test_report_create_unauthorized(self):
        c = Client()
        data = {
            'url': '/',
            'description': 'It doesn\'t work'
        }
        response = c.post('/report/', data, secure=True)
        reports = Report.objects.all()
        self.assertEqual(0, len(reports))

    def test_report_create(self):
        c = Client()
        c.login(username='ironman', password='imironman123')
        data = {
            'url': '/',
            'description': 'It doesn\'t work'
        }
        response = c.post('/report/', data, secure=True)
        reports = Report.objects.filter(responded=False)
        self.assertEqual(1, len(reports))

class ScrapeTestCase(TestCase):
    def setUp(self):
        Term.objects.create(value=42, name="The Answer")

    def test_scrape(self):
        self.do_scrape()

        logs = UpdateLog.objects.all()
        self.assertEqual(1, len(logs))
        log = logs[0]
        self.assertEqual(UpdateLog.SUCCESS, log.status)
        self.assertEqual(1, len(log.updates.all()))
        term_log = log.updates.all()[0]
        self.assertEqual(42, term_log.term.value)
        self.assertEqual(200, term_log.courses_parsed)
        self.assertEqual(103, term_log.courses_added)
        self.assertEqual(0, term_log.courses_updated)
        self.assertEqual(0, term_log.courses_deleted)

        term = Term.objects.get(value=42)
        courses = Course.objects.filter(term=term)
        deleted_courses = Course.objects.filter(term=term, deleted=True)
        hidden_courses = Course.objects.filter(term=term, hidden=True)
        self.assertEqual(term_log.courses_added, len(courses))
        self.assertEqual(0, len(deleted_courses))
        self.assertEqual(3, len(hidden_courses))

    def test_scrape_duplicate(self):
        self.do_scrape()
        self.do_scrape()

        logs = UpdateLog.objects.all()
        self.assertEqual(2, len(logs))
        log = logs[1]
        self.assertEqual(UpdateLog.SUCCESS, log.status)
        self.assertEqual(1, len(log.updates.all()))
        term_log = log.updates.all()[0]
        self.assertEqual(42, term_log.term.value)
        self.assertEqual(200, term_log.courses_parsed)
        self.assertEqual(0, term_log.courses_added)
        self.assertEqual(0, term_log.courses_updated)
        self.assertEqual(0, term_log.courses_deleted)

        term = Term.objects.get(value=42)
        courses = Course.objects.filter(term=term)
        deleted_courses = Course.objects.filter(term=term, deleted=True)
        hidden_courses = Course.objects.filter(term=term, hidden=True)
        self.assertEqual(103, len(courses))
        self.assertEqual(0, len(deleted_courses))
        self.assertEqual(3, len(hidden_courses))

    def test_scrape_with_updates(self):
        self.do_scrape()
        term = Term.objects.get(value=42)
        courses = Course.objects.filter(term=term).order_by('crn')
        for i in range(0, 10):
            course = courses[i]
            course.hours = 10
            course.save()
        for i in range(10, 20):
            course = courses[i]
            course.location = "ROOM 217"
            course.seats = 100
            course.deleted = True
            course.save()
        for i in range(20, 30):
            course = courses[i]
            course.delete()

        deleted_courses = Course.objects.filter(term=term, deleted=True)
        hidden_courses = Course.objects.filter(term=term, hidden=True)
        self.assertEqual(93, len(courses))
        self.assertEqual(10, len(deleted_courses))
        self.assertEqual(3, len(hidden_courses))

        self.do_scrape()

        logs = UpdateLog.objects.all()
        self.assertEqual(2, len(logs))
        log = logs[1]
        self.assertEqual(UpdateLog.SUCCESS, log.status)
        self.assertEqual(1, len(log.updates.all()))
        term_log = log.updates.all()[0]
        self.assertEqual(42, term_log.term.value)
        self.assertEqual(200, term_log.courses_parsed)
        self.assertEqual(10, term_log.courses_added)
        self.assertEqual(20, term_log.courses_updated)
        self.assertEqual(0, term_log.courses_deleted)

        courses = Course.objects.filter(term=term).order_by('crn')
        deleted_courses = Course.objects.filter(term=term, deleted=True)
        hidden_courses = Course.objects.filter(term=term, hidden=True)
        self.assertEqual(103, len(courses))
        self.assertEqual(0, len(deleted_courses))
        self.assertEqual(3, len(hidden_courses))
        for i in range(0, 10):
            course = courses[i]
            self.assertNotEqual(10, course.hours)
        for i in range(10, 20):
            course = courses[i]
            self.assertNotEqual("ROOM 217", course.location)
            self.assertNotEqual(100, course.seats)
            self.assertNotEqual(True, course.deleted)

    def do_scrape(self):
        args = [
            '--debug', 'n',
            '--output', 'n',
            '--local_data', 'y',
            '--local_data_term', '42',
            '--local_data_soc_source', '{}/static/assets/html/soc.html'.format(settings.BASE_DIR),
            '--local_data_fsoc_source', '{}/static/assets/html/fsoc.html'.format(settings.BASE_DIR),
        ]
        call_command('scrape-courses', *args)
