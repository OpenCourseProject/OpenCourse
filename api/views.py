from django.shortcuts import render
from django.http import HttpResponse
from course.models import Course, Term, Instructor
import json

def index(request):
    context = {}
    return render(request, 'api/index.html', context)

def course_all(request):
    data = []
    for course in Course.objects.all():
        data.append(course.to_json())
    return HttpResponse(data, 201)

def term_all(request):
    data = serializers.serialize("json", Term.objects.all())
    return HttpResponse(data, 201)

def instructor_all(request):
    data = serializers.serialize("json", Instructor.objects.all())
    return HttpResponse(data, 201)
