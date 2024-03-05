from peewee import MySQLDatabase

from .config import settings

database = MySQLDatabase(settings.DB_DATABASE,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                host=settings.DB_HOST,
                port=settings.DB_PORT)


