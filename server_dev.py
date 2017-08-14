import os

from pyserver.app.views import app
from werkzeug.contrib.fixers import ProxyFix

DEBUG = bool(os.environ.get('DEBUG', True))

app.wsgi_app = ProxyFix(app.wsgi_app)

def before_request():
    app.jinja_env.cache = {}

app.before_request(before_request)

if __name__ == '__main__':
    app.debug = DEBUG
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.testing=DEBUG
    app.static_folder = '/home/zanklord/webapps/walid/LinksBot/pyserver/static'
    port = int(os.environ.get('PORT', 8000))
    app.run(host='localhost', port=port)
