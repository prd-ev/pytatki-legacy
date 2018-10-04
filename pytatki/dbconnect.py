import pymysql
from pytatki.config import parse_config
from passlib.hash import sha256_crypt

__author__ = "Filip Wachowiak & Patryk Niedzwiedzinski"

CONFIG = parse_config('config.ini', check_db_configuration=False)

def connection(host=CONFIG['DATABASE']['DB_HOST'], user=CONFIG['DATABASE']['DB_USER'],
               password=CONFIG['DATABASE']['DB_PASSWORD'], db=CONFIG['DATABASE']['DB_NAME'],
               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db,
                           charset=charset,
                           cursorclass=cursorclass)
    c = conn.cursor()
    return c, conn

def create_usergroup(conn, name, description, parent_id='0'):
    """Insert usergroup into the database using given connection and returns its id"""
    conn.cursor().execute(
        "INSERT INTO usergroup (name, description) VALUES (%s, %s)", (pymysql.escape_string(name), pymysql.escape_string(description)))
    return conn.cursor().lastrowid

def create_status(conn, name, description):
    """Insert status into the database using given connection and returns its id"""
    conn.cursor().execute(
        "INSERT INTO status (name, description) VALUES (\"active\", \"Record is ative\")")
    return conn.cursor().lastrowid

def create_note_type(conn, name, description):
    """Insert note type into the database using given connection and returns its id"""
    conn.cursor().execute("INSERT INTO note_type (name, description) VALUES(%s, %s)", (pymysql.escape_string(name), pymysql.escape_string(description)))
    return conn.cursor().lastrowid

def create_user(conn, login, password, email, status_id):
    """Insert user into the database using given connection and returns its id"""
    conn.cursor().execute("INSERT INTO user (login, password, email, status_id) VALUES (%s, %s, %s, %s)", (
        pymysql.escape_string(login), pymysql.escape_string(
            sha256_crypt.encrypt(str(password))), pymysql.escape_string(email),
        pymysql.escape_string(str(status_id))))
    return conn.cursor().lastrowid
