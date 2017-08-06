import os

from peewee import *

DATABASE = os.environ.get("DATABASE", None)
print(DATABASE)
db = SqliteDatabase(DATABASE)
db.connect()


class User(Model):
    username = CharField()
    telegramId = CharField(unique=True)
    secret = CharField(unique=True)
    waitingReply = BooleanField(default=False)
    pocket_Token = CharField(null=True)
    pocket_configured = BooleanField(default=False)

    class Meta:
        database = db

class Link(Model):
    url = CharField()
    date = DateTimeField()
    private = BooleanField(default=True)
    user = ForeignKeyField(User)
    reviewed = BooleanField(default=False)

    class Meta:
        database = db
