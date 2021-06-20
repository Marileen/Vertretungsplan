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

    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum
    recipients = Subscriber.objects.all()

    for i in recipients:

        emailtest = EmailMessage('Testversand', 'Hallo ' + i.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.email])
        emailtest.attach_file('./downloads/' + date +".pdf")
        emailtest.send()

