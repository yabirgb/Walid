"""from flask import Flask
import os

app = Flask(__name__)


DEBUG = bool(os.environ.get('DEBUG', True))

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = DEBUG

port = int(os.environ.get('PORT', 8000))
app.run(host='localhost', port=port)
"""
