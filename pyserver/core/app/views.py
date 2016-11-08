from flask import render_template, redirect, request
from pymongo import MongoClient
from app import app

client = MongoClient('localhost', 27017)
db = client.test
collection = db.users


@app.template_filter('urls_completer')
def urls_completer(url):
    return url if "://" in url else "//" + url

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/secret/<secret>')
def user_links(secret):
    user = collection.find_one({"secret": secret})
    return render_template('links.html',
        user=user)

@app.route('/search/', methods=['GET', 'POST'])
def user_search():
    if request.args.get("code"):
        return redirect("/secret/{}".format(request.args.get("code")))
    return render_template('search.html')
 
@app.route('/about/')
def about():
    return render_template('about.html')
