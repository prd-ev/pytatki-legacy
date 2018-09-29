from config import CONFIG
import pymysql

__author__ = "Filip Wachowiak"


def connection():
    conn = pymysql.connect(host=CONFIG.DB_HOST,
                           user=CONFIG.DB_USER,
                           password=CONFIG.DB_PASSWORD,
                           db=CONFIG.DB_NAME,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    return c, conn
