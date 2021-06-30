# Vertretungsplan

Hier entsteht unser Projekt für das Auslesen der Vertretungspläne von Schulen, dass man benachrichtigt werden kann

## Nützliche Kommandos

###run server
<pre>python manage.py runserver</pre>

###Migrationen hinzufügen:
<pre>python manage.py makemigrations main</pre>

###Migrationen anwenden:
<pre>python manage.py migrate</pre>

###Shell (für Datenbank-Abfragen):
<pre>python manage.py shell</pre>

###Daten in DB hinzufügen und abfragen:

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

## Django Webpush

https://github.com/safwanrahman/django-webpush

Keys generieren: https://web-push-codelab.glitch.me/


## Notes

### Push Nachrichten 
Für Push Nachrichten gibt es verschiedene Möglichkeiten:
Wenn man die Website offen hat, gibt es Browser basierte Push Nachrichten
- notify.run: Free and open-source (lack of authentication) 
- Pushpad: Flexible notifications for developers to integrate into their own websites based on the web push notification standard.
- OneSignal: Free but explicitly indicate they sell you and your users data for their own profit1.
- Pushjet: Open-source framework used to develop your own push notification services. There are no user accounts, instead devices are subscribed to services (to which messages can be pushed).

ansonsten braucht man einen Provider wie 
- google cloud engine oder 
- Amazon SNS
- apple push

Es gibt auch Python Packages für Slack oder Telegramm

### SMS

- https://dev.telstra.com/