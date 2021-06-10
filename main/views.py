from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Grade

# Create your views here.


def index(response,id):
    school = School.objects.get(id=id)
    grade = school.grade_set.get(id=1)
    return HttpResponse("<h1>erster test: %s</h1><p>%s</p>" %(school.name, grade.name))
