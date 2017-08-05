from re import search
import uuid
import datetime
import os

import telebot
from peewee import *

TOKEN = os.environ.get("TOKEN", None)
DATABASE = os.environ.get("DATABASE", None)
from models import *

bot = telebot.TeleBot(TOKEN)

print("""
================
Bot started
================
"""
)




regex = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    user, created = User.get_or_create(telegramId=message.from_user.id,
                        username = message.from_user.username,
                        defaults={"secret":uuid.uuid4()})
    bot.reply_to(message, "Hi! I'm ready to store your links")

@bot.message_handler(regexp=regex)
def store_url(message):
    user, created = User.get_or_create(telegramId=message.from_user.id,
                        username = message.from_user.username,
                        defaults={"secret":uuid.uuid4()})
    positions = search(regex, message.text).span()
    Link.create(url=message.text[positions[0]:positions[1]], user = user, date =datetime.datetime.now(), private = True)
    bot.reply_to(message, "Link  saved!")

@bot.message_handler()
def handle_start_help(message):
	pass

bot.polling()
