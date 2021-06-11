from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Grade
from .forms import Subscribe
# Create your views here.


def index(response, id):
    school = School.objects.get(id=id)
    grades = school.grade_set.all()  # it's a QuerySet
    # return HttpResponse("<h1>erster test: %s</h1><p>%s</p>" %(school.name, grade.name))
    return render(response, "main/base.html", {})


def start(response):
    form = Subscribe()
    schools = School.objects.all()
    return render(response, "main/start.html", {"schools": schools, "form": form})
