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
    user = User()
    user.update(user_dict)
    con.close()
    conn.close()
    return user


@LM.user_loader
def user_load(user_id):
    try:
        con, conn = connection()
        con.execute("SELECT * FROM user WHERE iduser = %s",
                    escape_string(str(user_id)))
        user_dict = con.fetchone()
        user = User()
        user.update(user_dict)
        user.id = user_dict["iduser"]
        con.close()
        conn.close()
        gc.collect()
        return user
    except Exception as error:
        # TODO: exception type
        print(error)
        return None


class User(dict):
    def check_password(self, password):
        if sha256_crypt.verify(password, self['password']):
            return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        con, conn = connection()
        con.execute("SELECT * FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                    (escape_string(str(self['iduser'])), escape_string(Config['IDENTIFIERS']['admingroup_id'])))
        admin = con.fetchone()
        con.close()
        conn.close()
        if admin:
            return True
        return False

    def get_id(self):
        return unicode(self['iduser'])
