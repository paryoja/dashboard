"""Celery 설정."""
import os

from celery import Celery
from celery.schedules import crontab

# set the default Django my_settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.my_settings.production")

app = Celery("dashboard")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """디버깅용 celery 테스크."""
    print("Request: {0!r}".format(self.request))


app.conf.update(
    CELERYBEAT_SCHEDULE={
        "add-image": {
            "task": "book.views.views_api.cron_image_add",
            "schedule": crontab(hour="03", minute="20"),
        },
    }
)
