from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Grade, Subscriber
from .forms import Subscribe
# Create your views here.


def index(response, id):
    school = School.objects.get(id=id)
    grades = school.grade_set.all()  # it's a QuerySet
    # return HttpResponse("<h1>erster test: %s</h1><p>%s</p>" %(school.name, grade.name))
    return render(response, "main/base.html", {})


def start(response):

    schools = School.objects.all()

    if response.method == "POST":
        form = Subscribe(response.POST)

        if form.is_valid():
            firstname = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            s = Subscriber(name=firstname, email=email, telefon=phone)
            s.save()
            # return HttpResponseRedirect('/thanks/')
    else:
        form = Subscribe()
    return render(response, "main/start.html", {"schools": schools, "form": form})
