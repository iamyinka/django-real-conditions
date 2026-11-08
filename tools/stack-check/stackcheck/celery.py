import os

from celery import Celery

# The worker is its own process, so it needs to be told which settings to load.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stackcheck.settings")

app = Celery("stackcheck")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
