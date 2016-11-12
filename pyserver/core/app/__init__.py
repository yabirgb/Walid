from flask import Flask
import os

app = Flask(__name__)

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True

from app import views

port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port)
