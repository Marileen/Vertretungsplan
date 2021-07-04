import urllib.request
import os
from django.core.mail import EmailMessage
from main.models import *
from webpush import send_user_notification, send_group_notification
from django.core.exceptions import ObjectDoesNotExist
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
    filename = ''

    try:
        with urllib.request.urlopen(url) as f:
            pdf = f.read()
            if url.find('/'):
                filename = 'downloads/warbel/' + url.rsplit('/', 1)[1]
            open(filename, 'wb').write(pdf)
            print('Datei ' + filename + ' heruntergeladen')
    except urllib.request.HTTPError as exception:
        print('Error ' + filename + ' NICHT GELADEN')
        print(exception)


def send_messages(schoolname, directory, date, grades=None):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        school = School.objects.get(name__contains=schoolname)
    except:
       return

    try:
        subscriptions = Subscription.objects.filter(school=school)
    except:
        return

    if grades:
        # send only the info for desired grades to subscribers
        for sub in subscriptions:
            gradeName = sub.grade

            if gradeName and len(gradeName) > 0:
                payload = {"head": school.name + ' ' + sub.grade + ' Vertretungsinfo',
                           "body": grades.get(gradeName),
                           "icon": 'http://schmeckerly.de/vplan-icon.png',
                                   "url": school.url}
                try:
                    send_group_notification(group_name=school.id, payload=payload, ttl=1000)
                    # payload = {"head": 'TESTGROUP ' + school.name + ' ' + sub.grade + ' Vertretungsinfo',
                              #  "body": grades.get(gradeName),
                               # "icon": 'http://schmeckerly.de/vplan-icon.png',
                               # "url": school.url}
                    # send_group_notification(group_name='none', payload=payload, ttl=1000)
                except ObjectDoesNotExist:
                    pass

                mail = EmailMessage(school.name + ' ' + sub.grade + ' Vertretungsinfo',
                                        'Hallo ' + sub.subscriber.name +
                                        '. ' + grades.get(gradeName),
                                         to=[sub.subscriber.email])
                mail.send()

    else:
        # send mails with pdf attachment to subscribers for the schools that have pdf's
        # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum

        for i in subscriptions:
            mail = EmailMessage(school.name + ' Vertretungsinfo', 'Hallo ' + i.subscriber.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.subscriber.email])
            mail.attach_file('../downloads/' +directory +'/' + date +'.pdf')
            mail.send()


# Test-Funktion zum Versenden per Cronjob UND von der Website
def testmail():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # send mails with pdf attachment to "Kopernikus Gymnasium" subscribers
    test = EmailMessage('Testversand', 'Hallo. Hier kommt der aktuelle Vertretungsplan 2.', to=["wacker@online.de"])
    test.attach_file('../downloads/kopernikus/2021-06-11.pdf')
    test.send()
