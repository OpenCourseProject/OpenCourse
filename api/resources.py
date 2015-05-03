from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from course.models import Course, Term, Instructor

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
        #resource_name = 'course'
        allowed_methods = ['get']
        filtering = {
            'crn': ALL,
            'section': ALL,
            'title': ALL,
            'course': ALL,
            'hours': ALL,
            'llc': ALL,
            'ctype': ALL,
            'days': ALL,
            'start_time': ALL,
            'location': ALL,
            'seats': ALL,
            'status': ALL,
            'term': ALL_WITH_RELATIONS,
            'instructor': ALL_WITH_RELATIONS,
        }

class TestResource(ModelResource):
    class Meta:
        queryset = Instructor.objects.all()
        allowed_methods = ['get']
