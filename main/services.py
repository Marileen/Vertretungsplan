import os
import urllib.request
import urllib.error

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from webpush import send_group_notification
from main.models import *
from .vplan import VPlan


def filedownload_kopernikus():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum

    url = 'http://kgbe.de.w010c7c5.kasserver.com/Joomla/files/vplan/' + date + '.pdf'
    filename = ''

    with urllib.request.urlopen(url) as f:
        pdf = f.read()

    if url.find('/'):
        filename = '../downloads/kopernikus/' + url.rsplit('/', 1)[1]
    open(filename, 'wb').write(pdf)
    print('Datei ' + filename + ' heruntergeladen')


def filedownload_warbel():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # date = datetime.today().strftime('%d.%m.%Y') # aktuelles Tagesdatum
    date = '11.06.2021'  # ======> Testdatum
    # ======> warbel school is currently offline because of vacation
    # ======> url = 'http://www.warbel-schule-gnoien.de/.cm4all/uproc.php/0/' + date + '.pdf'
    # ======>  for demo, we are hosting some older file:
    url = 'http://schmeckerly.de/www.warbel-schule-gnoien.de/' + date + '.pdf'
    filename = ''

    try:
        with urllib.request.urlopen(url) as f:
            pdf = f.read()
            if url.find('/'):
                filename = '../downloads/warbel/' + url.rsplit('/', 1)[1]
            open(filename, 'wb').write(pdf)
            print('Datei ' + filename + ' heruntergeladen')
    except urllib.error.HTTPError as exception:
        print('Error ' + filename + ' NICHT GELADEN')
        print(exception)


def send_messages(schoolname, directory, date, grades=None):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        school = School.objects.get(name__contains=schoolname)
    except Exception as e:
        raise e

    try:
        subscriptions = Subscription.objects.filter(school=school)
    except Exception as e:
        raise e

    if grades:
        # send only the info for desired grades to subscribers
        for sub in subscriptions:
            grade_name = sub.grade

            if grade_name and len(grade_name) > 0:
                payload = {"head": school.name + ' ' + sub.grade + ' Vertretungsinfo',
                           "body": grades.get(grade_name),
                           "icon": 'http://schmeckerly.de/vplan-icon.png',
                           "url": school.url}
                try:
                    send_group_notification(group_name=str(school.id), payload=payload, ttl=1000)
                    # payload = {"head": 'TESTGROUP ' + school.name + ' ' + sub.grade + ' Vertretungsinfo',
                    #  "body": grades.get(grade_name),
                    # "icon": 'http://schmeckerly.de/vplan-icon.png',
                    # "url": school.url}
                    # send_group_notification(group_name='none', payload=payload, ttl=1000)
                except ObjectDoesNotExist:
                    pass

                mail = EmailMessage(school.name + ' ' + sub.grade + ' Vertretungsinfo',
                                    'Hallo ' + sub.subscriber.name +
                                    ',\n\nHier sind Deine aktuellen Vertretungsinfos:\n' + grades.get(
                                        grade_name) + '\n\nViele Grüße\nDein Team von Vertretungsplan24',
                                    to=[sub.subscriber.email])
                mail.send()

    else:
        # send mails with pdf attachment to subscribers for the schools that have pdf's
        # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum

        for i in subscriptions:
            mail = EmailMessage(school.name + ' Vertretungsinfo',
                                'Hallo ' + i.subscriber.name + ',\n\nhier kommt der aktuelle Vertretungsplan.' + '\n\nViele Grüße\nDein Team von Vertretungsplan24',
                                to=[i.subscriber.email])
            mail.attach_file('../downloads/' + directory + '/' + date + '.pdf')
            mail.send()


def run_plans():
    """
    gets VPlans and triggers the sending of e-mail and push notification
    for all schools
    """
    all_schools = School.objects.all()
    vplan = None

    filedownload_kopernikus()
    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    date = '2021-06-11'  # Testdatum
    send_messages('Kopernikus Gymnasium Bargteheide', 'kopernikus', date)
    filedownload_warbel()
    # date = datetime.today().strftime('%d.%m.%Y') # aktuelles Tagesdatum
    date = '11.06.2021'  # ======> Testdatum
    send_messages('Warbel-Schule Gnoien', 'warbel', date)

    for school in all_schools:
        # get VPlan's from schools that provides a website url
        if school.url:
            vplan = VPlan(school.name, school.url)
        if vplan and vplan.grades:
            send_messages(school, '', '', vplan.grades)
