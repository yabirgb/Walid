from re import search
import uuid
import datetime
import os
import json
from urllib.parse import quote_plus, urlparse
import time
import requests


from peewee import *
import peeweedbevolve
from telegram_bot.auth import hotp

from telegram_bot.models import User, Link, Map, Message

DB_NAME = "walid_test"
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

def urlNormalize(url):
    if not search(r'http', url):
        return "http://" + url
    else:
        return url

def fake_user():
    user, created = User.get_or_create(telegramId=0,
                        username = "yabir",
                        defaults={"authCode":0,
                        "secret":uuid.uuid4(), "pocket_configured":False})

    return user

def start():
    print("Starting creation of tables in " + str(DB_NAME))
    db.evolve([User, Link, Map, Message])
    print("Tables created")

def me(u="yabir"):
        user = fake_user()
        time = int(datetime.datetime.now().timestamp())
        q = User.update(authCode=time).where(User.username==u)
        num_of_row = q.execute()
        code = hotp.at(time)
        print ("Access to " + "http://walid.yabirgb.com" +"/secret/" + user.secret + "/" + str(code))

def store_url(url):
    user = fake_user()
    r = requests.get(urlNormalize(url))
    al = r.text
    title = al[al.find('<title>') + 7 : al.find('</title>')][:254]

    final_url = r.url
    Link.create(url=final_url, title=title, user = user, date =datetime.datetime.now(), private = True)
    print("Link  saved!")

if __name__ == '__main__':
    import sys
    if sys.argv[1] == "fake":
        fake_user()
    elif sys.argv[1] == "me":
        me()
    elif sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "save":
        store_url(sys.argv[2])
