__author__ = "Patryk Niedźwiedziński"
"""Skrypt tworzenia bazy danych"""

from sqlalchemy import create_engine
from dbconnect import connection
from pymysql import escape_string
from passlib.hash import sha256_crypt


def db_start():
    print("Connecting...")
    con, conn = connection()
    print("Connection OK")
    print("Setting up database...")
    con.execute("INSERT INTO usergroup (name, description) VALUES (\"admins\", \"group of admins\")")
    conn.commit()
    con.execute("INSERT INTO status (name, description) VALUES (\"active\", \"Record is ative\")")
    conn.commit()
    con.execute("SELECT idstatus FROM status WHERE name=\"active\"")
    status = con.fetchone()
    username = input("Insert your admin login: ")
    email = input("Insert your admin email: ")
    password = input("Insert your admin password: ")
    con.execute("INSERT INTO user (login, password, email, status_id) VALUES (%s, %s, %s, " + status['idstatus'] + ")", (escape_string(username), escape_string(email), escape_string(sha256_crypt(password))))
    con.close()
    conn.close()


if __name__ == '__main__':
    db_start()
