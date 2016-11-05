from flask import render_template
from pymongo import MongoClient
from app import app

client = MongoClient('localhost', 27017)
db = client.test
collection = db.users

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/secret/<secret>')
def user_links(secret):
    user = collection.find_one({"secret": secret})
    return render_template('links.html',
        user=user)
