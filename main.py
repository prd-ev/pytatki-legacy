'''Plik glowny aplikacji'''

import os
from config import CONFIG
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://8fd621a0050d43e993c78fa1764ba1be@sentry.io/1286329",
    integrations=[FlaskIntegration()]
)

__author__ = 'Patryk Niedzwiedzinski'

def create_app(test_config=None):
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    APP.static_path = os.path.join(os.path.abspath(__file__), 'static')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        APP.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        APP.config.update(test_config)
    return APP

APP = create_app()
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=CONFIG.EMAIL,
    MAIL_PASSWORD=CONFIG.EMAIL_PASSWORD
)
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login_get'
BCRYPT = Bcrypt()
MAIL = Mail(APP)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
