"""Modele rekordów wpisywanych do bazy danych"""
from flask_login import UserMixin
from numpy import unicode
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from passlib.hash import sha256_crypt
from main import DB, LM

__author__ = 'Patryk Niedźwiedziński'

@LM.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))

class User(DB.Model):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    username = Column(String(20), unique=True)
    email = Column(String(200))
    confirm_mail = Column(Boolean, default=True)
    password = Column(String(200), default='')
    modderator = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    superuser = Column(Boolean, default=False)
    ban = Column(Boolean, default=False)

    def check_password(self, password):
        if sha256_crypt.verify(password, self.password):
            return True

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Note(DB.Model):
    __tablename__ = 'note'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
    author_id = Column(Integer)
    subject_id = Column(Integer)
    topic_id = Column(Integer)
    date = Column(String(20))


class Topic(DB.Model):
    __tablename__ = 'topic'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
    subject_id = Column(Integer)

class Subject(DB.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(200))
