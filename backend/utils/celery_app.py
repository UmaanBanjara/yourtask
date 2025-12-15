from celery import Celery
from celery.schedules import crontab

#celery config
celery_app = Celery(
    "yourtask",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.beat_scheduler = {
    'customer-daily-report' : {
        'task' : 'backend.tasks.customer_tasks.send_customer_details',
        'schedule' : crontab(hour=15 , minute=0) #everyday at 8am
    }
}


import backend.tasks.customer_tasks