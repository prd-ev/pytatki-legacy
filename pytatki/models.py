# -*- coding: utf-8 -*-
"""Database tables models"""
from flask_login._compat import unicode
from passlib.hash import sha256_crypt
from pytatki.main import LM
from pytatki.dbconnect import connection
from pymysql import escape_string
import gc
from pytatki.main import CONFIG as Config


def get_user(id_user=None, login=None, email=None):
    """Returns user by given data"""
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
    if not user_dict:
        return None
    con.execute("SELECT * FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                (escape_string(str(user_dict['iduser'])), escape_string(str(Config['database']['admingroup_id']))))
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
