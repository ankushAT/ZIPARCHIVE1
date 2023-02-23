import os
from celery import Celery
from .settings import CELERY_broker_url
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zipArchive.settings')

app = Celery('zipArchive', broker=CELERY_broker_url)


# from zipdir.tasks import create_archive
# app.task(create_archive)

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):    
    print(f'Request: {self.request!r}')

    