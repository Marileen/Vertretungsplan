from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import School, Grade, Subscriber, Subscription
from .forms import Subscribe, Subscriptions
from django.db import IntegrityError
from django.contrib import messages
# Create your views here.


def index(response, id):
    school = School.objects.get(id=id)
    grades = school.grade_set.all()  # it's a QuerySet
    # return HttpResponse("<h1>erster test: %s</h1><p>%s</p>" %(school.name, grade.name))
    return render(response, "main/base.html", {})


def start(response):

    schools = School.objects.all()
    form_subscribe = Subscribe(response.POST)

    if response.method == "POST":

        if form_subscribe.is_valid():
            firstname = form_subscribe.cleaned_data["name"]
            email = form_subscribe.cleaned_data["email"]
            phone = form_subscribe.cleaned_data["phone"]
            subscr = Subscriber(name=firstname, email=email, telefon=phone)

            try:
                subscr.save()

                # create a subscription for the user for a school
                school = form_subscribe.cleaned_data["school"]
                subscription = Subscription(school=school, subscriber=subscr)
                subscription.save()

            except IntegrityError as e:
                if 'unique constraint' in e.args[0]:  # or e.args[0] from Django 1.10
                    return HttpResponseRedirect('/duplicate/')

            messages.success(response, "Erfolgreich angemeldet für <strong>"
                             + str(form_subscribe.cleaned_data["school"]) + "</strong>")
            return HttpResponseRedirect('/thanks/')

    return render(response, "main/start.html", {"schools": schools, "form_subscribe": form_subscribe})


def edit(response):
    return render(response, "main/edit-subscriptions.html", {})


def thanks(response):
    subscriptions_form = Subscriptions(response.POST)
    return render(response, "main/thanks.html", {"form_subscriptions": subscriptions_form})

