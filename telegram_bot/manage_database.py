from peewee import *
from models import *
import datetime
import random

import telebot

TOKEN = os.environ.get("TOKEN", None)
bot = telebot.TeleBot(TOKEN)

def start():
    print("Starting creation of tables in " + str(DATABASE))
    db.evolve([User, Link, Map, Message])
    print("Tables created")

def users_count():
    print(len(User.select()))

def clean_auth():
    query = User.update(authCode=0).where()

def cycle_code():
    time = int(datetime.datetime.now().timestamp())
    a = datetime.datetime.now() - datetime.timedelta(minutes=25)
    reduction = int(a.timestamp())
    q = User.update(authCode=random.randint(0, time)).where(User.authCode < reduction )
    num_of_row = q.execute()

    print("Auth code modifications: " + str(num_of_row))

def send_mess(pk, message):
    bot.send_message(pk, message)

def bulk(message):
    for u in User.select():
        send_mess(u.telegramId, message)


if __name__ == '__main__':
    import sys
    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "users":
        users_count()
    elif sys.argv[1] == "codes":
        cycle_code()
    elif sys.argv[1] == "send":
        send_mess(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "bulk":
        bulk(sys.argv[2])
