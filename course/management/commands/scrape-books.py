from django.core.management.base import BaseCommand, CommandError
from course.models import Course, Material
from lxml import html
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Course.objects.all()
        for course in query:
            if course.bookstore_link:
                page = requests.get(course.bookstore_link)
                tree = html.fromstring(page.text)
                result = tree.xpath('//div[@class="material-group-overview"]')

                materials = []
                for value in result:
                    materials.append(Material(title=value.xpath('h3/text()')[0].strip().encode('ascii','ignore')))
                prop = []
                result = tree.xpath('//div[@class="material-group-edition"]')
                for i in range(0, len(materials)):
                    value = result[i]
                    list = value.xpath('span/text()')
                    try:
                        Material.objects.get(isbn=int(list[2].strip()), term=course.term, course_crn=course.crn)
                    except Material.DoesNotExist:
                        materials[i].term = course.term
                        materials[i].course_crn = course.crn
                        materials[i].author = list[0].strip()
                        materials[i].edition = list[1].strip()
                        materials[i].isbn = int(list[2].strip())
                        if list[3].strip().isdigit():
                            materials[i].year = int(list[3].strip())
                        materials[i].save()
