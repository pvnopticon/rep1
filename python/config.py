from flask import request, Flask
import configparser
from peewee import *
import psycopg2

app = Flask(__name__)
# Загрузка стандартных настроек
app.config.from_object(__name__)

# Инициализация БД
config = configparser.ConfigParser()  # создаём объекта парсера
config.read('python/config.ini')
db = PostgresqlDatabase(
    config['DB']['dbname'],  # Required by Peewee.
    host=config['DB']['host'],
    user=config["DB"]['user'],
    password=config['DB']['password']
)


class BaseModel(Model):
    class Meta:
        database = db