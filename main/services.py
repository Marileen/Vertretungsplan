import urllib.request
from django.core.mail import EmailMessage
from main.models import *
from datetime import datetime


def filedownload():

    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum

    url = 'http://kgbe.de.w010c7c5.kasserver.com/Joomla/files/vplan/' + date + '.pdf'

    with urllib.request.urlopen(url) as f:
        pdf = f.read()

    if url.find('/'):
        filename = 'downloads/' + url.rsplit('/', 1)[1]
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
        emailtest.attach_file('./downloads/' + date +".pdf")
        emailtest.send()

