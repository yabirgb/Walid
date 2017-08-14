from re import search
import uuid
import datetime
import os
import json
from urllib.parse import quote_plus, urlparse
import time

import requests
from lxml.html import fromstring
import telebot

from peewee import *

from models import *
from auth import hotp

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

def create_or_get_user(message):
    user, created = User.get_or_create(telegramId=message.from_user.id,
                        username = message.from_user.username,
                        defaults={"authCode":0,
                        "secret":uuid.uuid4(), "pocket_configured":False})
    return user

regex = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
regex_pocket = r'!p '

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = create_or_get_user(message)
    user.waitingReply = False
    user.save()
    text = """
    * Send me any url and it will be stored. If it is mixed with text, I will found it! 👍🏼
    \n* To configure your pocket account use `/pocket` and follow the instructions
    \n* Display all your urls using `/me` and visit the url 💻
    \n* To store a location share it using telegram's ubication share 📲
    \n* Save a message typing `/m text_to_send` ✉️
    \n* Saving urls to pocket is easy, use the sintax `!p url tag1 tag2 ...` 😄
    \nIf you still have problems contact @yabir on telegram.
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    user = create_or_get_user(message)
    text = """
    * Send me any url and it will be stored. If it is mixed with text, I will found it! 👍🏼
    \n* To configure your pocket account use `/pocket` and follow the instructions
    \n* Display all your urls using `/me` and visit the url 💻
    \n* To store a location share it using telegram's ubication share 📲
    \n* Save a message typing `/m text_to_send` ✉️
    \n* Saving urls to pocket is easy, use the sintax `!p url tag1 tag2 ...` 😄
    \nIf you still have problems contact @yabir on telegram.
    """
    bot.reply_to(message, text)

@bot.message_handler(commands=["stop"])
def stop(message):
    user = User.get(telegramId=message.from_user.id)
    q = User.update(waitingReply=True).where(User.telegramId==message.from_user.id)
    num_of_row = q.execute()

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
            bot.reply_to(message, "Link saved to your pocket!")
        else:
            bot.reply_to(message, "Oh no! Something went wrong")


@bot.message_handler(regexp=regex)
def store_url(message):
    user = create_or_get_user(message)
    positions = search(regex, message.text).span()
    url = message.text[positions[0]:positions[1]]

    try:
        r = requests.get(urlNormalize(url))
        tree = fromstring(r.content)
        title = str(tree.findtext('.//title'))
        final_url = r.url
        Link.create(url=final_url, title=title, user = user, date =datetime.datetime.now(), private = True)
        bot.reply_to(message, "Link  saved!")
    except:
        bot.reply_to(message, "Something strange with this url")




@bot.message_handler(commands=['pocket'])
def pocket_login(message):
    mess = "Click on {} to login".format(BASE_URL + "/pocket/" + str(message.from_user.id))
    bot.reply_to(message, mess)

@bot.message_handler(commands=["me"])
def links(message):
    user = User.get(telegramId=message.from_user.id)
    time = int(datetime.datetime.now().timestamp())
    q = User.update(authCode=time).where(User.telegramId==message.from_user.id)
    num_of_row = q.execute()
    code = hotp.at(time)
    bot.reply_to(message, "Access to " + BASE_URL+"/secret/" + user.secret + "/" + code)

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")


@bot.message_handler(commands=["m"])
def store_message(message):
    user = create_or_get_user(message)
    Message.create(text=message.text[3:], reviewed= False, user = user, date =datetime.datetime.now())
    bot.reply_to(message, "Message saved")

@bot.message_handler(content_types=["location"])
def store_map(message):
    user = create_or_get_user(message)
    Map.create(latitude=message.location.latitude, longitude=message.location.longitude, reviewed = False, user = user, date =datetime.datetime.now())
    bot.reply_to(message, "Location saved")

bot.polling()
