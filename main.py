'''Plik główny aplikacji'''

import os
from config import CONFIG
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail

__author__ = 'Patryk Niedźwiedziński'

def create_app():
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    APP.static_path = os.path.join(os.path.abspath(__file__), 'static')
    return APP

APP = create_app()
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=CONFIG.EMAIL,
    MAIL_PASSWORD=CONFIG.EMAIL_PASSWORD
)
DB = SQLAlchemy()
DB.app = APP
DB.init_app(APP)
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login'
BCRYPT = Bcrypt()
MAIL = Mail(APP)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    from src.views import *
    from src.user import *
    APP.run(debug=CONFIG.DEBUG, host=CONFIG.HOST, port=CONFIG.PORT, ssl_context=CONFIG.SSL_CONTEXT)