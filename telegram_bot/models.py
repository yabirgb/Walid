import os

from peewee import *
import peeweedbevolve
from playhouse.hybrid import hybrid_property


DEBUG = bool(os.environ.get("DEBUG", False))
DATABASE = os.environ.get("DATABASE", "")
MAPS = os.environ.get("MAPS", "")

if DEBUG == None:
    db = SqliteDatabase(DATABASE)
else:
    DB_NAME = os.environ.get("DB", None)
    DB_USER = os.environ.get("DBUSER", None)
    DB_PASS = os.environ.get("DBPASS", None)
    DB_HOST = os.environ.get("DBHOST", None)
    db = PostgresqlDatabase(
        DB_NAME,  # Required by Peewee.
        user=DB_USER,  # Will be passed directly to psycopg2.
        password=DB_PASS,  # Ditto.
        host=DB_HOST,  # Ditto.
    )

db.get_conn()


class User(Model):
    username = CharField(null=True)
    telegramId = CharField(unique=True)
    secret = CharField(unique=True)
    authCode = IntegerField()
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
    title = CharField()

    class Meta:
        database = db

class Map(Model):
    latitude = DoubleField()
    longitude = DoubleField()
    reviewed = BooleanField(default=False)
    date = DateTimeField()
    user = ForeignKeyField(User)

    @hybrid_property
    def maps(self):
        url ="https://www.google.com/maps/embed/v1/view?key={}&center={},{}&zoom={}&maptype={}"
        zoom = 16
        view = "satellite"
        return url.format(MAPS, self.latitude, self.longitude, zoom, view)


    class Meta:
        database = db

class Message(Model):
    date = DateTimeField()
    text = CharField(max_length=500)
    reviewed = BooleanField(default=False)
    user = ForeignKeyField(User)
    class Meta:
        database = db
