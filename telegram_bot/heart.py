from re import search
import uuid
import datetime
import os
import json
from urllib.parse import quote_plus, urlparse
import time

import requests
import telebot
from peewee import *

from models import *

TOKEN = os.environ.get("TOKEN", None)
DATABASE = os.environ.get("DATABASE", None)
POCKET = os.environ.get("POCKET", None)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
headers = {'Content-Type' : 'application/json; charset=UTF-8','X-Accept': 'application/json'}


bot = telebot.TeleBot(TOKEN)

print("""
================
Bot started
================
"""
)

def urlNormalize(url):
    if not search(r'http:\/\/', url):
        return "http://" + url
    else:
        return url


regex = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
regex_pocket = r'!p '

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(POCKET)
    user, created = User.get_or_create(telegramId=message.from_user.id,
                        username = message.from_user.username,
                        defaults={"secret":uuid.uuid4(), "pocket_configured":False})
    bot.reply_to(message, "Hi! I'm ready to store your links")

@bot.message_handler(regexp=regex_pocket)
def store_pocket(message):
    user = User.get(telegramId=message.from_user.id)
    if user.pocket_configured == True:
        code = user.pocket_Token
        data = message.text.split(" ")
        url = data[1]
        tags = (",").join(data[2:])

        r_url = requests.get(urlNormalize(url))
        final_url = r_url.url
        payload = dict(consumer_key=POCKET, access_token=code, url=final_url, tags=tags )
        print(json.dumps(payload))
        r = requests.post('https://getpocket.com/v3/add', data=json.dumps(payload), headers=headers)
        print(r.headers)

        if(r.status_code == 200):
            bot.reply_to(message, "Link  saved to your pocket!")
        else:
            bot.reply_to(message, "Oh no! Something went wrong")


@bot.message_handler(regexp=regex)
def store_url(message):
    user, created = User.get_or_create(telegramId=message.from_user.id,
                        username = message.from_user.username,
                        defaults={"secret":uuid.uuid4(), "pocket_configured":False})
    positions = search(regex, message.text).span()
    Link.create(url=message.text[positions[0]:positions[1]], user = user, date =datetime.datetime.now(), private = True)
    bot.reply_to(message, "Link  saved!")


@bot.message_handler(commands=['pocket'])
def pocket_login(message):
    mess = "Click on {} to login".format(BASE_URL + "/pocket/" + str(message.from_user.id))
    bot.reply_to(message, mess)

@bot.message_handler(commands=["me"])
def on_ping(message):
    user = User.get(telegramId=message.from_user.id)
    bot.reply_to(message, BASE_URL+"/secret/" + user.secret)

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")

bot.polling()
