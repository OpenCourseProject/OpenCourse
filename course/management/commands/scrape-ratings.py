from django.core.management.base import BaseCommand, CommandError
from course.models import Instructor
from lxml import html
import requests
import decimal

BASE_URL = "http://www.ratemyprofessors.com"
SEARCH_URL = BASE_URL + "/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName=Christopher+Newport+University&query="

class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Instructor.objects.all()
        for instructor in query:
            if instructor.last_name != "Staff" and not instructor.rmp_link:
                page = requests.get(SEARCH_URL + instructor.last_name)
                tree = html.fromstring(page.text)
                result = tree.xpath('//li[@class="listing PROFESSOR"]')
                found = False
                for value in result:
                    if found:
                        break
                    names = value.xpath('//span[@class="listing-name"]/span[@class="main"]/text()')[0]
                    arr = names.split(", ")
                    if arr[1].startswith(instructor.first_name):
                        if len(arr[1]) > len(instructor.first_name):
                            instructor.first_name = arr[1]
                        link = value.xpath('a')[0].get('href')
                        instructor.rmp_link = BASE_URL + link
                        found = True
                        instructor.save()
        for instructor in query:
            if instructor.rmp_link:
                page = requests.get(instructor.rmp_link)
                tree = html.fromstring(page.text)
                result = tree.xpath('//div[@class="grade"]/text()')
                if result and len(result) > 0:
                    value = decimal.Decimal(result[0])
                    instructor.rmp_score = value
                    instructor.save()
        self.stdout.write('Successfully ran RMP lookup')
