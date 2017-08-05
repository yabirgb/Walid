from peewee import *
from models import *


def start():
    if not User.table_exists():
        db.create_tables([User, Link])


start()
