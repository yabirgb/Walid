from flask import Flask
import os

app = Flask(__name__)


DEBUG = os.environ.get('DEBUG', True)
if DEBUG == "False":
    DEBUG = False

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = DEBUG

#from pyserver.core.app import views

#port = int(os.environ.get('PORT', 8000))
#app.run(host='0.0.0.0', port=port)
