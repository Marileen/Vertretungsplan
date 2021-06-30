import urllib.request
from django.core.mail import EmailMessage
from main.models import *
from webpush import send_user_notification, send_group_notification
from datetime import datetime


def filedownload_kopernikus():

    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum

    url = 'http://kgbe.de.w010c7c5.kasserver.com/Joomla/files/vplan/' + date + '.pdf'

    with urllib.request.urlopen(url) as f:
        pdf = f.read()

    if url.find('/'):
        filename = 'downloads/kopernikus/' + url.rsplit('/', 1)[1]
    open(filename, 'wb').write(pdf)
    print('Datei ' + filename + ' heruntergeladen')


def filedownload_warbel():

    # date = datetime.today().strftime('%d.%m.%Y') # aktuelles Tagesdatum
    date = '11.06.2021'  # Testdatum

    url = 'http://www.warbel-schule-gnoien.de/.cm4all/uproc.php/0/' + date + '.pdf'

    with urllib.request.urlopen(url) as f:
        pdf = f.read()

    if url.find('/'):
        filename = 'downloads/warbel/' + url.rsplit('/', 1)[1]
    open(filename, 'wb').write(pdf)
    print('Datei ' + filename + ' heruntergeladen')


def sendmail():

    # send mails with pdf attachment to "Kopernikus Gymnasium" subscribers
    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum
    school_kopernikus = School.objects.get(name__contains='Kopernikus Gymnasium Bargteheide')
    subscriptions_kopernikus = Subscription.objects.filter(school=school_kopernikus)

    for i in subscriptions_kopernikus:

        emailtest = EmailMessage('Testversand', 'Hallo ' + i.subscriber.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.subscriber.email])
        emailtest.attach_file('./downloads/kopernikus/' + date +".pdf")
        emailtest.send()


    date_warbel = '11.06.2021'  # Testdatum
    school_warbel = School.objects.get(name__contains='Warbel-Schule Gnoien')
    subscriptions_warbel = Subscription.objects.filter(school=school_warbel)

    for i in subscriptions_warbel:

        emailtest = EmailMessage('Testversand', 'Hallo ' + i.subscriber.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.subscriber.email])
        emailtest.attach_file('./downloads/warbel/' + date_warbel +".pdf")
        emailtest.send()


def sendmail2(schoolname, directory, date, grades=None):

    if grades:
        # send only the info for desired grades to subscribers
        print('todo: hier messages mit klassen-info senden')
        payload = {"head": "Welcome!", "body": "Hello World"}
        send_group_notification(group_name="test", payload=payload, ttl=1000)

    else:
        # send mails with pdf attachment to subscribers for the schools that have pdf's
        # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
        school = School.objects.get(name__contains=schoolname)
        subscriptions = Subscription.objects.filter(school=school)

        for i in subscriptions:

            emailtest = EmailMessage('Testversand', 'Hallo ' + i.subscriber.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.subscriber.email])
            emailtest.attach_file('./downloads/' +directory +'/' + date +'.pdf')
            emailtest.send()
