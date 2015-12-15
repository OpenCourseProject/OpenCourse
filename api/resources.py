from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from course.models import Course, Term, Instructor, MeetingTime, Attribute, Material, FollowEntry, CourseVersion
from schedule.models import ScheduleEntry

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
            'rmp_link': ALL,
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

class MeetingTimeResource(ModelResource):
    class Meta:
        queryset = MeetingTime.objects.all()
        resource_name = 'meeting time'
        allowed_methods = ['get']
        filtering = {
            'days': ALL,
            'start_time': ALL,
            'end_time': ALL,
        }

class CourseResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)
    instructor = fields.ToOneField(InstructorResource, 'instructor', full=True)
    meeting_times = fields.ToManyField(MeetingTimeResource, 'meeting_times', full=True)

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        allowed_methods = ['get']
        filtering = {
            'term': ALL_WITH_RELATIONS,
            'crn': ALL,
            'course': ALL,
            'course_link': ALL,
            'section': ALL,
            'title': ALL,
            'bookstore_link': ALL,
            'hours': ALL,
            'attribute': ALL,
            'ctype': ALL,
            'meeting_times': ALL_WITH_RELATIONS,
            'location': ALL,
            'instructor': ALL_WITH_RELATIONS,
            'seats': ALL,
            'status': ALL,
        }

class MaterialResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)

    class Meta:
        queryset = Material.objects.all()
        resource_name = 'material'
        allowed_methods = ['get']
        filtering = {
            'term': ALL_WITH_RELATIONS,
            'course_crn': ALL,
            'isbn': ALL,
            'title': ALL,
            'author': ALL,
            'publisher': ALL,
            'edition': ALL,
            'year': ALL,
        }

class CourseVersionResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)

    class Meta:
        queryset = CourseVersion.objects.all()
        resource_name = 'courseversion'
        allowed_methods = ['get']
        filtering = {
            'term': ALL_WITH_RELATIONS,
            'course_crn': ALL,
            'time_created': ALL,
        }

class CRNValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'No data provided.'}

        errors = {}

        term = bundle.data.get('term').split('/')[4]
        course_crn = bundle.data.get('course_crn')
        try:
            Course.objects.get(term=term, crn=course_crn)
        except Course.DoesNotExist:
            errors['course_crn'] = ['Course does not exist for this term.']

        return errors

class ScheduleResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)

    class Meta:
        queryset = ScheduleEntry.objects.all()
        resource_name = 'schedule'
        allowed_methods = ['get', 'post', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = CRNValidation()
        filtering = {
            'course_crn': ALL,
            'term': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        return super(ScheduleResource, self).obj_create(bundle, user=bundle.request.user)

    def get_object_list(self, request):
        return super(ScheduleResource, self).get_object_list(request).filter(user=request.user)

class FollowResource(ModelResource):
    term = fields.ToOneField(TermResource, 'term', full=True)

    class Meta:
        queryset = FollowEntry.objects.all()
        resource_name = 'follow'
        allowed_methods = ['get', 'post', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = CRNValidation()
        filtering = {
            'course_crn': ALL,
            'term': ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        return super(FollowResource, self).obj_create(bundle, user=bundle.request.user)

    def get_object_list(self, request):
        return super(FollowResource, self).get_object_list(request).filter(user=request.user)
