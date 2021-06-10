from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Grade

# Create your views here.


def index(response,id):
    school = School.objects.get(id=id)
    return HttpResponse("<h1>erster test: %s</h1>" % school.name)
