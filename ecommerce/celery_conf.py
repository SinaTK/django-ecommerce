from celery import Celery
from datetime import timedelta
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

celery_app = Celery('ecommerce')
celery_app.autodiscover_tasks()

# celery_app.conf.broker_url = 'amqp://guest:guest@localhost'  # run on django server
celery_app.conf.broker_url = 'amqp://guest:guest@rabbitmq'  # run on docker
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 3

