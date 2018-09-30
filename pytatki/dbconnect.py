import pymysql
from pytatki.config import parse_config

__author__ = "Filip Wachowiak"

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
