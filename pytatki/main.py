"""Plik glowny aplikacji"""

import os
from config import CONFIG
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask

__author__ = 'Patryk Niedzwiedzinski'


def create_app(test_config=None):
    app = Flask(__name__)
    app.static_path = os.path.join(os.path.abspath(__file__), 'static')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    return app


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
