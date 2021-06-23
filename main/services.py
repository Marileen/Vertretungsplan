import urllib.request
from django.core.mail import EmailMessage
from bs4 import BeautifulSoup
from main.models import *
from datetime import datetime


class VPlan:
    def __init__(self, name, url):
        self.website = self.gethtml('https://gms-kellinghusen.de/vertretungsplan.html')
        self.name = name
        self.grades = self.getGrades()

    def gethtml(self, url):
        # url = 'https://gms-kellinghusen.de/vertretungsplan.html'

        with urllib.request.urlopen(url) as f:
            plan = f.read()

        soup = BeautifulSoup(plan, 'html.parser')
        return soup

    def getGrades(self):

        grades = []
        grade_nodes = self.website.select('.v-klasse')

        for grade in grade_nodes:
            grades.append(grade.text)

        print(grades)

        return grades



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

def sendmail2(schoolname, directory, date):

    # send mails with pdf attachment to "Kopernikus Gymnasium" subscribers
    # date = datetime.today().strftime('%Y-%m-%d') # aktuelles Tagesdatum
    school = School.objects.get(name__contains=schoolname)
    subscriptions = Subscription.objects.filter(school=school)

    for i in subscriptions:

        emailtest = EmailMessage('Testversand', 'Hallo ' + i.subscriber.name +'. Hier kommt der aktuelle Vertretungsplan.' , to=[i.subscriber.email])
        emailtest.attach_file('./downloads/' +directory +'/' + date +'.pdf')
        emailtest.send()
