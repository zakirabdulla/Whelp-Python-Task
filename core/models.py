import datetime

from peewee import Model, CharField, DateTimeField, ForeignKeyField
from playhouse.mysql_ext import JSONField

from app.db import database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)


class Task(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = ForeignKeyField(User, backref='tasks')
    uid = CharField(unique=True,null=True)
    status = CharField(choices=STATUS_CHOICES, default='pending')
    ip = CharField()
    data = JSONField()

