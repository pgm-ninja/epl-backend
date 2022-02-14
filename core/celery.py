from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from core.settings.current_env import django_setup

django_setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.staging.staging')
app = Celery('core')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'load_data_periodically': {
        'task': 'services.tasks.weekly_data_load',
        'schedule': crontab(hour=7, minute=45, day_of_week=0)
    },

    'save_data_periodically': {
        'task': 'services.tasks.weekly_data_save',
        'schedule': crontab(hour=7, minute=47, day_of_week=0)
    },

    'save_model_periodically': {
        'task': 'services.tasks.weekly_model_save',
        'schedule': crontab(hour=7, minute=50, day_of_week=0)
    }

}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'request:{self.request!r}')