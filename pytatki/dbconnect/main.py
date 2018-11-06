"""Main functions"""
import pymysql
from pytatki.config import parse_config

__author__ = "Patryk Niedźwiedziński"


CONFIG = parse_config('config.json', check_db_configuration=False)


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


def add_user_to_usergroup(conn, iduser, idusergroup):
    """Add user to usergroup"""
    c = conn.cursor()
    c.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)",
              (pymysql.escape_string(str(iduser)), pymysql.escape_string(str(idusergroup))))
    return c.lastrowid
