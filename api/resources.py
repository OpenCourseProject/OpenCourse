from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from course.models import Course, Term, Instructor, Attribute, Material

class TermResource(ModelResource):
    class Meta:
        queryset = Term.objects.all()
        resource_name = 'term'
        allowed_methods = ['get']
        filtering = {
            'value': ALL,
            'name': ALL,
        }

class InstructorResource(ModelResource):
    class Meta:
        queryset = Instructor.objects.all()
        resource_name = 'instructor'
        allowed_methods = ['get']
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
            'rmp_score': ALL,
        }

class CourseResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)
    instructor = fields.ToOneField(InstructorResource, 'instructor', full=True)

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        allowed_methods = ['get']
        filtering = {
            'crn': ALL,
            'section': ALL,
            'title': ALL,
            'course': ALL,
            'hours': ALL,
            'attribute': ALL,
            'ctype': ALL,
            'days': ALL,
            'start_time': ALL,
            'location': ALL,
            'seats': ALL,
            'status': ALL,
            'term': ALL_WITH_RELATIONS,
            'instructor': ALL_WITH_RELATIONS,
        }

class AttributeResource(ModelResource):
    class Meta:
        queryset = Attribute.objects.all()
        resource_name = 'attribute'
        allowed_methods = ['get']
        filtering = {
            'value': ALL,
            'name': ALL,
        }

class MaterialResource(ModelResource):
    course = fields.ToOneField(CourseResource, 'course')

    class Meta:
        queryset = Material.objects.all()
        resource_name = 'material'
        allowed_methods = ['get']
        filtering = {
            'isbn': ALL,
            'title': ALL,
            'author': ALL,
            'publisher': ALL,
            'edition': ALL,
            'year': ALL,
            'course': ALL_WITH_RELATIONS,
        }
