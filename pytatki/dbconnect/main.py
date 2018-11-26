"""Main functions"""
import pymysql
from pytatki.config import parse_config

__author__ = "Patryk Niedźwiedziński"


CONFIG = parse_config('config.json', check_db_configuration=False)


def connection(host=CONFIG['database']['db_host'], user=CONFIG['database']['db_user'],
               password=CONFIG['database']['db_password'], db=CONFIG['database']['db_name'],
               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
    conn = pymysql.connect(host=host,
                           port=3306,
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
    c.execute("SELECT 1 FROM user_membership WHERE usergroup_id = %s AND user_id = %s",
              (pymysql.escape_string(str(idusergroup)), pymysql.escape_string(str(iduser))))
    if c.fetchone():
        return "user already a member"
    c.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)",
              (pymysql.escape_string(str(iduser)), pymysql.escape_string(str(idusergroup))))
    return c.lastrowid
