"""Plik glowny aplikacji"""

import os
from pytatki.config import parse_config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
from celery import Celery
from whitenoise import WhiteNoise

__author__ = 'Patryk Niedzwiedzinski'


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


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
    print("An error occurred while parsing config file")
    exit("Error")

APP = create_app()
APP.config.update(
    MAIL_SERVER=CONFIG['email']['mail_server'],
    MAIL_PORT=CONFIG['email']['mail_port'],
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=CONFIG['email']['email'],
    MAIL_PASSWORD=CONFIG['email']['email_password'],
    MAIL_DEFAULT_SENDER=CONFIG['email']['email']
)
<< << << < HEAD
APP.config['CELERY_RESULT_BACKEND'] = 'rpc://'
APP.config['CELERY_BROKER_URL'] = 'amqp://localhost'
== == == =

APP.wsgi_app = WhiteNoise(APP.wsgi_app, root='pytatki/static')
>>>>>> > master
LM = LoginManager()
LM.init_app(APP)
LM.login_view = 'login_get'
BCRYPT = Bcrypt()
MAIL = Mail(APP)
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'files')
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CELERY = make_celery(APP)
