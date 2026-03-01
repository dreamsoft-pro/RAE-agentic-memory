import pymysql
from .my_celery_app import app as celery_app

pymysql.install_as_MySQLdb()
