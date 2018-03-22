__author__ = 'Patryk Niedźwiedziński'
'''Skrypt tworzenia bazy danych'''

from sqlalchemy import create_engine
from main import DB
import models
from passlib.hash import sha256_crypt


def db_start():
    engine = create_engine('sqlite:///tmp/test.db', convert_unicode=True)
    DB.create_all()
    DB.session.commit()

    user = models.User()
    user.username = "patryk"
    user.password = sha256_crypt.encrypt("h@sl0")
    user.email = 'pniedzwiedzinski19@gmail.com'
    user.admin = True
    DB.session.add(user)
    DB.session.commit()

if __name__ == '__main__':
    db_start()
