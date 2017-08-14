import os
import requests
import json

from flask import (Flask,render_template, redirect, request, abort, jsonify)

from peewee import *
from playhouse.shortcuts import model_to_dict
from htmlmin.minify import html_minify
import peeweedbevolve

from telegram_bot.models import User, Link, Map, Message
from telegram_bot.auth import hotp

app = Flask(__name__)

DEBUG = bool(os.environ.get("DBDEBUG", True))
if DEBUG == True:
    print("yeah")
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


POCKET = os.environ.get("POCKET", None)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
REDIRECT_URL = BASE_URL + '/auth/{}'

headers = {'Content-Type' : 'application/json; charset=UTF-8','X-Accept': 'application/json'}
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
"""
@app.template_filter('urls_completer')
def urls_completer(url):
    return url if "://" in url else "//" + url

@app.route('/')
@app.route('/index')
def index():
    html = render_template('index.html',title='Home')
    return html_minify(html)

@app.route('/changelog')
def changelog():
    html = render_template('changelog.html',title='changelog')
    return html_minify(html)

@app.route('/secret/<secret>/<code>')
def user_links(secret, code):
    """Fetch links for an user.

    Args:
        Secret: A secret code generated by uuid that identifies the user.
        Code: An OTP code generated by telegram app.

    Returns:
        Minified version of the list with links, maps and messages if the
        secret matchs the code at  the moment.
    """
    try:
        user = User.get(User.secret==secret)
    except:
        return "403 - Secret code invalid"

    print(code, user.authCode)
    if hotp.verify(code, user.authCode):
        links =Link.select().join(User).where(User.secret==secret).dicts()
        maps = [model_to_dict(x, extra_attrs=["maps"], exclude=["latitude", "longitude"],
                    recurse=False) for x in Map.select().join(User).where(User.secret==secret)]
        messages = Message.select().join(User).where(User.secret==secret).dicts()

        links_json = json.dumps({'data':list(links)},sort_keys=True, default=str)
        maps_json = json.dumps({'data':list(maps)},sort_keys=True, default=str)
        messages_json = json.dumps({'data':list(messages)},sort_keys=True, default=str)

        html = render_template('links.html',
                                user=user, urls=links_json, maps=maps_json,
                                messages=messages_json, secret=secret , code=code)
        return html_minify(html)

    else:
        return "403 - Auth code error"

@app.route('/search/', methods=['GET', 'POST'])
def user_search():
    if request.args.get("code"):
        return redirect("/secret/{}".format(request.args.get("code")))
    return render_template('search.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/pocket/<tid>')
def get_pocket(tid):
    """Get token from pocket api to login user

    Args:
        tid: Telegram user id that identifies user.

    Returns:
        Error code or redirects to the authorize page of pocket
    """

    user = User.get(User.telegramId==tid)
    if user.pocket_configured == True:
        return "Already configured"

    r_url = REDIRECT_URL.format(tid)
    payload = dict(consumer_key=POCKET, redirect_uri=r_url)
    r = requests.post('https://getpocket.com/v3/oauth/request', data=json.dumps(payload), headers=headers)

    if r.status_code == 200:
        code = r.json()["code"]
        print(code)
        q = User.update(pocket_Token=code).where(User.telegramId==tid)
        q.execute()
        auth_url = "https://getpocket.com/auth/authorize?request_token={}&redirect_uri={}".format(code, r_url)
        return redirect(auth_url)
    else:
        return str(r.status_code)

@app.route('/auth/<tid>')
def auth(tid):
    """Authorize user on pocket app

    Args:
        tid: Telegram user id that identifies user.

    Returns:
        Error code or redirects to the main page if success
    """
    user = User.get(User.telegramId==tid)
    if user.pocket_configured == True:
        return "Pocket already configured"

    code = user.pocket_Token
    print(code)
    payload = {"code":code, "consumer_key": POCKET}
    r = requests.post("https://getpocket.com/v3/oauth/authorize", data=json.dumps(payload),  headers=headers)
    if r.status_code == 200:
        data = r.json()
        user = User.get(User.telegramId==tid)
        q = User.update(pocket_Token=data["access_token"], pocket_configured=True).where(User.telegramId==tid)
        num_of_row = q.execute()
        print("Token: ", data["access_token"], "\n")
        return redirect("/")
    else:
        print(r.headers)
        return str(r.status_code)

# ========
# Api
# ========
@app.route('/api/<secret>/<code>/<obj>/<pk>')
def toggle_show(secret, code, obj, pk):

    try:
        user = User.get(User.secret==secret)
    except:
        return "403 - Secret code invalid"
    if hotp.verify(code, user.authCode):
        if obj == "link":
            link = Link.get(Link.id == pk)
            link.reviewed = not link.reviewed
            link.save()

            links =Link.select().join(User).where(User.secret==secret).dicts()
            response_code = 200

            return jsonify( response_code = 200, data =list(links) )

        elif obj == "maps":
            location = Map.get(Map.id == pk)
            location.reviewed = not location.reviewed
            location.save()
            return "ok"
        elif obj == "messages":
            message = Message.get(Message.id == pk)
            message.reviewed = not message.reviewed
            message.save()
            return "ok"
        else:
            return "404"
    else:
        return "403"
