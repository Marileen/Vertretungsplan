import main.services

def my_scheduled_job():
    # hier die Funktionen, die per Cronjob ausgeführt werden sollen
    main.services.testmail()


    # Cronjobs "aktivieren"
    # python manage.py crontab add

    # Aktive Cronjobs anzeigen
    # python manage.py crontab show

    # Alle Cronjobs von Crontabs entfernen
    # python manage.py crontab remove