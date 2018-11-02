from init_db import db_init
import pymysql
import pytest


def generator():
    yield "127.0.0.1"
    yield "root"
    yield None
    yield "admin"
    yield "test@admin"
    yield "12345"


input_generator = generator()


@pytest.mark.last
def test_db_init(monkeypatch):
    conn = pymysql.connect(host='127.0.0.1', user='pytatki', password='pytatki', charset="utf8mb4",
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    c.execute("DROP DATABASE pytatki")
    conn.close()
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    db_init()
