from datetime import datetime

from celery import shared_task

@shared_task()
def common():
    print(datetime.today())