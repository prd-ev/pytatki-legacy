# -*- coding: utf-8 -*-
"""This module contains models for all objects in the app."""

import gc

from flask_login._compat import unicode
from passlib.hash import sha256_crypt
from pymysql import escape_string

from pytatki import __version__ as version
from pytatki.dbconnect import connection
from pytatki.main import CONFIG as Config
from pytatki.main import LM

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


def get_user(id_user=None, login=None, email=None):
    """Generates user object with data fetched from database."""
    sql = "SELECT * FROM user WHERE {} = %s"
    user_data = ()
    if id_user:
        sql = sql.format("iduser")
        user_data = (escape_string(str(id_user)))
    elif login:
        sql = sql.format("login")
        user_data = (escape_string(login))
    elif email:
        sql = sql.format("email")
        user_data = (escape_string(email))
    con, conn = connection()
    con.execute(sql, user_data)
    user_dict = con.fetchone()
    if user_dict is None:
        con.close()
        conn.close()
        gc.collect()
        return None
    con.execute("SELECT * FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                (escape_string(str(user_dict['iduser'])), escape_string(str(Config['identifiers']['admingroup_id']))))
    admin = con.fetchone()
    user = User(is_admin=bool(admin))
    user.update(user_dict)
    con.close()
    conn.close()
    gc.collect()
    return user


@LM.user_loader
def user_load(user_id):
    try:
        user = get_user(id_user=user_id)
        user.id = user["iduser"]
        return user
    except Exception as error:
        # TODO: exception type
        print(error)
        return None


class User(dict):
    def __init__(self, is_admin):
        self.is_admin = is_admin

    def __repr__(self):
        return "User: {}".format(self['login'])

    def check_password(self, password):
        if sha256_crypt.verify(password, self['password']):
            return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self['iduser'])
