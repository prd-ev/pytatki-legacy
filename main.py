'''Plik główny aplikacji'''

from os import path
from config import Localhost
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

__author__ = 'Patryk Niedźwiedziński'

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy()
DB.app = APP
DB.init_app(APP)
LM = LoginManager()
LM.init_app(APP)
BCRYPT = Bcrypt()
CONFIG = Localhost

APP.static_path = path.join(path.abspath(__file__), 'static')


if __name__ == '__main__':
    from views import *
    APP.run(debug=CONFIG.DEBUG, host=CONFIG.HOST, port=CONFIG.PORT)
