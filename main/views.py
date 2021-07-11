from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import School, Subscriber, Subscription
from .forms import Subscribe, Subscriptions
from .services import run_plans
from .vplan import VPlan


def index(response, id):
    return render(response, "main/base.html", {})


def fetch_grades(request):
    """
    Endpoint for serving grade data by school_id
    :return JsonResponse
    """
    data = {}

    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        school_id = post_data.get("school_id")

        if len(school_id) < 1:
            school_id = 0
        try:
            school = School.objects.get(id=school_id)
            vplan = VPlan(school.name, school.url)
            data = {
                'grades': vplan.gradeList
            }
        except Exception as exc:
            pass

    return JsonResponse(data)


def start(response):
    """
    Provides Registration Form and Saves Subcriber and Subscriptions
    :return HTML
    """
    schools = School.objects.all()
    form_subscribe = Subscribe(response.POST)
    webpush = {"group": 'test'}
    done_register = None

    if response.method == "POST":

        if form_subscribe.is_valid():
            firstname = form_subscribe.cleaned_data["name"]
            email = form_subscribe.cleaned_data["email"]
            school = form_subscribe.cleaned_data["school"]
            grade = response.POST.get('grade')
            # phone = form_subscribe.cleaned_data["phone"]
            subscr = Subscriber(name=firstname, email=email)
            done_register = 1
            messages.success(response, "Du bist erfolgreich angemeldet für <strong>"
                                       + str(form_subscribe.cleaned_data["school"]) + " " + "</strong>")

            try:
                subscr.save()

            except IntegrityError as e:
                if 'email' in e.args[0]:  # or e.args[0] from Django 1.10
                    subscr = Subscriber.objects.get(email=email)
                # elif 'phone' in e.args[0]:
                # subscr = Subscriber.objects.get(phone=phone)
                else:
                    raise e

            # create a subscription for the user for a school
            subscription = Subscription(school=school, subscriber=subscr, grade=grade)

            try:
                subscription.save()
                emailconfirm = EmailMessage('Anmeldebestätigung Vertretungsinfo',
                                            'Hallo ' + firstname + ',\nvielen Dank für deine Anmeldung.\n\nAb sofort bekommst Du an jedem Schultag automatisch die aktuellsten Vertretungsinfos für die folgende Schule:\n' + str(
                                                form_subscribe.cleaned_data[
                                                    "school"]) + '\n\nViele Grüße\nDein Team von Vertretungsplan24',
                                            to=[email])
                emailconfirm.send()

                # save school as groupname for web push notifications
                webpush = {"group": school.name}

            except IntegrityError as e:
                if 'unique constraint' in e.args[0]:
                    messages.info(response, "Sie sind bereits registriert für die Schule <strong>"
                                     + str(form_subscribe.cleaned_data["school"]) + "</strong>")
                else:
                    messages.info(response, "Das hat nicht geklappt, weil: " + e.args[0])

    return render(response, "main/start.html", {
        "schools": schools,
        "form_subscribe": form_subscribe,
        "webpush": webpush,
        "done_register": done_register
    })


def edit(response):
    """
    Provides Form to query Subscriptions and delete them
    :return HTML
    """
    subscriptions_form = Subscriptions(response.POST)
    info = ''
    entries = None
    email = ''

    if response.method == "POST":

        # LÖSCHEN
        if response.POST.get("delete_subscription"):
            try:
                del_subscr = Subscription.objects.get(id=response.POST.get("subscription_id"))
                del_subscr.delete()
                info = del_subscr.school.name + ' - ' + (del_subscr.grade if del_subscr.grade else '') + " gelöscht"
            except Exception as e:
                raise e

        # ABFRAGEN
        elif response.POST.get("email") and subscriptions_form.is_valid():
            email = subscriptions_form.cleaned_data["email"]
            info = "Keine Daten gefunden"

            # Django DB Query
            try:
                subscriber = Subscriber.objects.get(email=email)
                entries = Subscription.objects.filter(subscriber=subscriber)
                if entries and len(entries) > 0:
                    info = "Folgende Einträge gefunden"
            except ObjectDoesNotExist as e:
                pass
                # if 'not exist' in e.args[0]:  # or e.args[0] from Django 1.10
                # info = "nix"

    return render(response, "main/edit-subscriptions.html", {
        "form_subscriptions": subscriptions_form,
        "info": info,
        "entries": entries,  # entry.school if entry else None
        "subscriber": email
    })


def thanks(response):
    """
    Thank you page
    :return HTML
    """
    subscriptions_form = Subscriptions(response.POST)
    return render(response, "main/thanks.html", {"form_subscriptions": subscriptions_form})


def send(response):
    """
    Trigger Sending via Webpage to test this project
    :return HTML
    """
    all_subscriptions = Subscription.objects.all()

    if response.method == "POST":
        if response.POST.get("send"):
            run_plans()

    return render(response, "main/send-messages.html", {
        "sub": all_subscriptions,
    })
