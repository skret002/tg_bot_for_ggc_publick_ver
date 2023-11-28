from celery import Celery
from celery.schedules import crontab

app = Celery('ggc')
default_config = 'tasks.celeryconfig'
app.config_from_object(default_config)

app.conf.beat_schedule = {
    'task_notis': {
        'task': 'notis',
        'schedule': 60.0,
    },
    'task_chenge_settings': {
        'task': 'change_settings',
        'schedule': 120.0,
    },
    'task_respons_support': {
        'task': 'resp_support',
        'schedule': crontab('0','*', '*', '*', '*'),
    },
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
