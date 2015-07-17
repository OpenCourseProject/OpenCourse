from django.core.management.base import BaseCommand, CommandError
from course.models import Course, Material
from lxml import html
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Course.objects.all()
        self.stdout.write('Gathering materials for ' + str(query.count()) + ' courses...')
        for course in query:
            if course.bookstore_link:
                page = requests.get(course.bookstore_link)
                tree = html.fromstring(page.text)
                materials = []
                # Check for package first
                titles = tree.xpath('//h3[@class="material-group-title clsTitle"]/text()')
                if len(titles) == 0:
                    # No packages, just use regular listings
                    titles = tree.xpath('//h3[@class="material-group-title"]/text()')
                for value in titles:
                    title = value.strip().encode('ascii','ignore')
                    if len(title) > 0:
                        materials.append(Material(title=title))
                prop = []
                result = tree.xpath('//div[@class="material-group-edition"]')
                for i in range(0, len(materials)):
                    value = result[i]
                    list = value.xpath('span/text()')
                    existing_materials = Material.objects.filter(term=course.term, course_crn=course.crn)
                    found = False
                    for entry in existing_materials:
                        # Search by ISBN
                        if list[2].strip().isdigit():
                            if entry.isbn and entry.isbn == int(list[2].strip()):
                                # Update details
                                entry.title = materials[i].title
                                entry.author = list[0].strip()
                                entry.edition = list[1].strip()
                                if list[3].strip().isdigit():
                                    entry.year = int(list[3].strip())
                                entry.save()
                                found = True
                                break
                        else:
                            if entry.title == materials[i].title:
                                # Update details
                                entry.author = list[0].strip()
                                entry.edition = list[1].strip()
                                if list[2].strip().isdigit():
                                    entry.isbn = int(list[2].strip())
                                if list[3].strip().isdigit():
                                    entry.year = int(list[3].strip())
                                entry.save()
                                found = True
                                break
                    # Save a new copy
                    if not found:
                        materials[i].term = course.term
                        materials[i].course_crn = course.crn
                        materials[i].author = list[0].strip()
                        materials[i].edition = list[1].strip()
                        if list[2].strip().isdigit():
                            materials[i].isbn = int(list[2].strip())
                        if list[3].strip().isdigit():
                            materials[i].year = int(list[3].strip())
                        materials[i].save()
        self.stdout.write('Finished lookup.')
