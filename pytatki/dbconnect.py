import pymysql
from pytatki.config import parse_config

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
    group_id = conn.cursor().lastrowid
    return group_id

def create_status(conn, name, description):
    """Insert status into the database using given connection and returns its id"""
    conn.cursor().execute(
        "INSERT INTO status (name, description) VALUES (\"active\", \"Record is ative\")")
    active_id = conn.cursor().lastrowid
    return active_id
