# Vertretungsplan

Reads content from HTML Website and downloads PDF files 
from School Websites to provide Vertretungsplan Information 
to Subscribers

## Useful Commands

## Installation
<pre>pip install -r requirements.txt</pre>

>> You also need the secret.py file for credentials of webpush and mail

### run server
<pre>python manage.py runserver</pre>

### Migrationen hinzufügen:
<pre>python manage.py makemigrations main</pre>

### Migrationen anwenden:
<pre>python manage.py migrate</pre>

### Shell (für Datenbank-Abfragen):
<pre>python manage.py shell</pre>

### Daten in DB hinzufügen und abfragen:

1) Starte shell: <pre>python manage.py shell</pre>
2) Commands:
    <pre>from main.models import Grade, School
   s = School(name="Kopernikus Gymnasium Bargteheide")
   s.save()
   
   // Abfragen:
   School.objects.all()
   School.objects.get(id=1)
   School.objects.get(name="Kopernikus Gymnasium Bargteheide")
   
   //Related items einfügen
   s.grade_set.create(name="5a")
   
   //Item-Set abfragen
   s.grade_set.all()
   s.grade_set.get(id=1)
   s.filter(name__startswith="Ko")
   //löschen
   del_object = s.get(id=1)
   de_object.delete()
</pre>



## Admin Dashboard
<pre>python manage.py createsuperuser</pre>
user: franz
email: franz@th-luebeck.de
pw: fgq5%tth

# Used Packages

## Beautiful Soup
For reading from Website

## Django Crontab
To schedule a job that triggers sending of messages

## Django Webpush
To send browser notifications
https://github.com/safwanrahman/django-webpush