import ipdata

from .app import celery_app

from app.db import database
from app.config import settings

from core.models import Task

@celery_app.task
def add(x, y):
    s =  x + y
    print(s)
    return s

@celery_app.task()
def fetch_ip_data(db_task_id:int):
    database.connect()
    ipdata.api_key = settings.IPDATA_API_KEY
    db_task = Task.get(Task.id == db_task_id)
    try:
        data = ipdata.lookup(db_task.ip)
    except Exception as e:
        db_task.status = "failed"
        db_task.data = {"error":str(e)}
    else:
        db_task.status = "completed"
        db_task.data = data
    db_task.save()
    database.close()

