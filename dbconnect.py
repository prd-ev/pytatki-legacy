from config import CONFIG
import pymysql

__author__ = "Filip Wachowiak"

def connection():
    conn = pymysql.connect(host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            db=DB_NAME,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    return c, conn