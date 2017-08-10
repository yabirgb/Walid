import os

from pyserver.app.views import app
from werkzeug.contrib.fixers import ProxyFix

DEBUG = bool(os.environ.get('DEBUG', True))

app.static_folder = '/home/zanklord/webapps/walid/LinksBot/pyserver/static'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = DEBUG

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.debug = DEBUG
    port = int(os.environ.get('PORT', 8000))
    app.run(host='localhost', port=port)
