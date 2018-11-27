"""This module creates the flask app instance and configure all services."""

import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from whitenoise import WhiteNoise

from pytatki import __version__ as version
from pytatki.config import parse_config

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


def create_app(test_config=None):
    app = Flask(__name__)
    app.static_path = os.path.join(os.path.abspath(__file__), 'static')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py', silent=True)
        pass
    else:
        # load the test config if passed in
        app.config.update(test_config)
    return app


CONFIG = parse_config('config.json')
if CONFIG is None:
    raise Exception("An error occurred while parsing config file")

APP = create_app()
APP.config.update(
    MAIL_SERVER=CONFIG['email']['mail_server'],
    MAIL_PORT=CONFIG['email']['mail_port'],
    MAIL_USE_TLS=CONFIG['email']['mail_use_tls'],
    MAIL_USE_SSL=CONFIG['email']['mail_use_ssl'],
    MAIL_USERNAME=CONFIG['email']['email'],
    MAIL_PASSWORD=CONFIG['email']['email_password'],
    MAIL_DEFAULT_SENDER=CONFIG['email']['email']
)

APP.wsgi_app = WhiteNoise(APP.wsgi_app, root='pytatki/static')
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login_get'
MAIL = Mail(APP)
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'files')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
