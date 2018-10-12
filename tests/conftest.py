from pytatki.main import create_app
import pytest
import pymysql
from pytatki.dbconnect import connection, create_user, create_status, create_usergroup, add_user_to_usergroup, create_notegroup, create_note_type, create_note, remove_notegroup
from pytatki.views import type_id, has_access_to_usergroup
from init_db import parse_sql
from shutil import copy
from pytatki.config import parse_config


@pytest.fixture(scope='session', autouse=True)
def create_db():
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE \'pytatki\'")
    db_exists = cursor.fetchone()
    if db_exists:
        raise Warning("Database exists")
    for query in parse_sql('sql/create-database.sql'):
        print(query)
        cursor.execute(query)
    cursor.execute("SELECT User FROM mysql.user WHERE User=\"pytatki\" AND Host=\"127.0.0.1\"")
    user_exists = cursor.fetchone()
    if not user_exists:
        cursor.execute("CREATE USER \'pytatki\'@\'127.0.0.1\' IDENTIFIED BY \'pytatki\';")
    cursor.execute("GRANT ALL ON pytatki.* TO \'pytatki\'@\'127.0.0.1\'")
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def insert_active_status(create_db):
    _, conn = connection()
    conn.begin()
    create_status(conn, 'active', 'Record is active')
    conn.commit()
    _.close()
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def insert_removed_status(insert_active_status):
    c, conn = connection()
    conn.begin()
    create_status(conn, 'removed', 'Record is removed')
    conn.commit()
    c.close()
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def insert_user(insert_active_status):
    _, conn = connection()
    conn.begin()
    user_id = create_user(conn, 'test', 'test', 'test@test', 1)
    conn.commit()
    _.close()
    conn.close()
    return user_id


@pytest.fixture(scope='session', autouse=True)
def insert_usergroup(insert_user):
    _, conn = connection()
    conn.begin()
    usergroup_id = create_usergroup(conn, 'test', 'test')
    add_user_to_usergroup(conn, insert_user, usergroup_id)
    conn.commit()
    _.close()
    conn.close()
    return usergroup_id


@pytest.fixture(scope='function', autouse=True)
def insert_notegroup(insert_usergroup, insert_user):
    def _insert(*args, **kwargs):
        _, conn = connection()
        conn.begin()
        notegroup_id = create_notegroup(*args, **kwargs)
        conn.commit()
        _.close()
        conn.close()
        return notegroup_id
    return _insert


@pytest.fixture(scope='session', autouse=True)
def insert_test_notegroup(insert_usergroup, insert_user):
    _, conn = connection()
    conn.begin()
    notegroup_id = create_notegroup(conn, 'test', insert_usergroup)
    conn.commit()
    _.close()
    conn.close()
    return notegroup_id


@pytest.fixture(scope='session', autouse=True)
def insert_text_note_type(create_db):
    _, conn = connection()
    conn.begin()
    note_type_id = create_note_type(conn, 'text', 'Text')
    conn.commit()
    _.close()
    conn.close()
    return note_type_id


@pytest.fixture(scope='session', autouse=True)
def insert_note(insert_user, insert_text_note_type, insert_test_notegroup):
    """Insert new note"""
    con, conn = connection()
    conn.begin()
    note_id = create_note(
        conn, 'test', 'Test', insert_text_note_type, insert_user, insert_test_notegroup, 1)
    conn.commit()
    con.close()
    conn.close()
    return note_id
