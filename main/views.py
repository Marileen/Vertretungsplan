from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .models import School, Subscriber, Subscription
from .forms import Subscribe, Subscriptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.mail import EmailMessage
from .services import filedownload_kopernikus, filedownload_warbel
from .vplan import VPlan

from .services import send_messages


def index(response, id):
    school = School.objects.get(id=id)
    return render(response, "main/base.html", {})


def fetch_grades(request):
    """
    Endpoint for serving grade data by school_id
    :return JsonResponse
    """
    data = {}
    vPlan = None

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

    schools = School.objects.all()
    form_subscribe = Subscribe(response.POST)
    webpush = {"group": 'test'}

    if response.method == "POST":

        if form_subscribe.is_valid():
            firstname = form_subscribe.cleaned_data["name"]
            email = form_subscribe.cleaned_data["email"]
            # phone = form_subscribe.cleaned_data["phone"]
            subscr = Subscriber(name=firstname, email=email)

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
            school = form_subscribe.cleaned_data["school"]
            grade = response.POST.get('grade')
            subscription = Subscription(school=school, subscriber=subscr, grade=grade)

            try:
                subscription.save()
                emailconfirm = EmailMessage('Anmeldebestätigung', 'Body', to=[email])
                emailconfirm.send()

                # save school as groupname for web push notifications
                webpush = {"group": school.name}

                messages.success(response, "Erfolgreich angemeldet für <strong>"
                                 + str(form_subscribe.cleaned_data["school"]) + "</strong>")
            except IntegrityError as e:
                if 'unique constraint' in e.args[0]:
                    messages.success(response, "Sie sind bereits registiert für die Schule <strong>"
                                     + str(form_subscribe.cleaned_data["school"]) + "</strong>")

            return HttpResponseRedirect('/thanks/')

    return render(response, "main/start.html", {
        "schools": schools,
        "form_subscribe": form_subscribe,
        "webpush": webpush,
    })


def edit(response):
    subscriptions_form = Subscriptions(response.POST)
    info = '---'
    entries = None
    email = ''

    if response.method == "POST":

        # LÖSCHEN
        if response.POST.get("delete_subscription"):
            subscriber = Subscriber.objects.get(email=response.POST.get("subscriber"))
            school = School.objects.get(name=response.POST.get("school"))
            try:
                del_subscr = Subscription.objects.get(subscriber=subscriber, school=school)
                del_subscr.delete()
                info = str(school) + " gelöscht"
            except Exception as e:
                raise e
                info = "Fehler - Löschung konnte nicht durchgeführt werden"

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
    subscriptions_form = Subscriptions(response.POST)
    return render(response, "main/thanks.html", {"form_subscriptions": subscriptions_form})


def send(response):
    """
    - gets VPlans and triggers the sending of e-mail and push notification
        for all schools
    - renders send-messages.html
    """
    all_subscriptions = Subscription.objects.all()
    all_schools = School.objects.all()
    vplan = None

    if response.method == "POST":
        if response.POST.get("send"):
            filedownload_kopernikus()
            send_messages('Kopernikus Gymnasium Bargteheide', 'kopernikus', '2021-06-11')
            filedownload_warbel()
            send_messages('Warbel-Schule Gnoien', 'warbel', '11.06.2021')

            for school in all_schools:
                # get VPlan's from schools that provides a website url
                if school.url:
                    vplan = VPlan(school.name, school.url)
                if vplan and vplan.grades:
                    send_messages(school, '', '', vplan.grades)

    return render(response, "main/send-messages.html", {
        "sub": all_subscriptions,
    })

