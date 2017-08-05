import os

from flask import render_template, redirect, request
from pyserver.core.app import app
from peewee import *

from telegram_bot.models import User, Link

DATABASE = os.environ.get("DATABASE", None)

db = SqliteDatabase(DATABASE)
db.connect()

@app.template_filter('urls_completer')
def urls_completer(url):
    return url if "://" in url else "//" + url

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/secret/<secret>')
def user_links(secret):
    user = User.get(User.secret==secret)
    links =Link.select().join(User).where(User.secret==secret)
    return render_template('links.html',
        user=user, urls=links)

@app.route('/search/', methods=['GET', 'POST'])
def user_search():
    if request.args.get("code"):
        return redirect("/secret/{}".format(request.args.get("code")))
    return render_template('search.html')

@app.route('/about/')
def about():
    return render_template('about.html')
