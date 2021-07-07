from main.services import run_plans


def my_scheduled_job():
    run_plans()

    # Cronjobs "aktivieren"
    # python manage.py crontab add

    # Aktive Cronjobs anzeigen
    # python manage.py crontab show

    # Alle Cronjobs von Crontabs entfernen
    # python manage.py crontab remove
