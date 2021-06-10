# Vertretungsplan

Hier entsteht unser Projekt für das Auslesen der Vertretungspläne von Schulen, dass man benachrichtigt werden kann

## Nützliche Kommandos

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
</pre>

