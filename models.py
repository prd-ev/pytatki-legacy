"""Modele rekordów wpisywanych do bazy danych"""

from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from main import DB

__author__ = 'Patryk Niedźwiedziński'


class User(DB.Model, UserMixin):
    """
    User model for reviewers.
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    username = Column(String(20), unique=True)
    email = Column(String(200))
    password = Column(String(200), default='')
    admin = Column(Boolean, default=False)

    def is_active(self):
        """
        Returns if user is active.
        """
        return self.active

    def is_admin(self):
        """
        Returns if user is admin.
        """
        return self.admin
