from celery import Celery

from app.config import settings

celery_app = Celery('whelp_celery', 
        broker=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/', backend='rpc://')

# celery_app.conf.task_routes = {
#     'celery_tasks.tasks.add': {'queue': 'add'},
# }


celery_app.conf.update(
    CELERY_IMPORTS=("celery_tasks.tasks"),
)
