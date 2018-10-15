# -*- coding: utf-8 -*-
"""Database tables models"""
from flask_login._compat import unicode
from passlib.hash import sha256_crypt
from pytatki.main import LM
from pytatki.dbconnect import connection
from pymysql import escape_string
import gc
from pytatki.main import CONFIG as Config


@LM.user_loader
def user_load(user_id):
    try:
        con, conn = connection()
        con.execute("SELECT * FROM user WHERE iduser = %s",
                    escape_string(str(user_id)))
        user_dict = con.fetchone()
        user = User()
        user.update(user_dict)
        con.close()
        conn.close()
        gc.collect()
        return user
    except:
        return None


class User(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

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
        query = con.execute("SELECT * FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                            (escape_string(self['userid']), escape_string(Config.json()['admin_group_id'])))
        con.close()
        conn.close()
        if query:
            return True
        return False

    def get_id(self):
        return unicode(self['iduser'])
