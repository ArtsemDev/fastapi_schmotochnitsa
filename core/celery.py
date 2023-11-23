from celery import Celery
from celery.schedules import crontab

from core.settings import settings

celery = Celery()
celery.config_from_object(obj=settings, namespace="CELERY")
celery.autodiscover_tasks(packages=["core"])
celery.conf.beat_schedule = {
    "long-ping": {
        "task": "core.tasks.long_ping",
        "schedule": crontab(minute="*")
    }
}
