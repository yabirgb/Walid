import os

from pyserver.app.views import app

DEBUG = bool(os.environ.get('DEBUG', True))

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.debug = DEBUG

if __name__ == '__main__':
    app.debug = DEBUG
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    app.run(host=host, port=port)
