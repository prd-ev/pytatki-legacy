from flask import g
from flask_httpauth import HTTPBasicAuth
from pytatki.models import User
from passlib.hash import sha256_crypt
from dbconnect import connection
from pymysql import escape_string

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    con, conn = connection()
    con.execute("SELECT password FROM user WHERE login = %s", escape_string(username))
    user_dict = con.fetchone()
    user = User()
    user.update(user_dict)
    con.close()
    conn.close()
    if not user or not sha256_crypt.verify(password, user['password']):
        return False
    return True


