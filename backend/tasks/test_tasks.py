from backend.utils.celery_app import celery_app

@celery_app.task
def test_task():
    print('Celery is working')
    return "Your Task"