import json

import pymysql

from init_db import parse_sql
from pytatki.dbconnect import (connection, create_action, create_note,
                               create_note_type, create_notegroup,
                               create_status, create_user, create_usergroup,
                               has_access_to_note, note_exists,
                               notegroup_empty, remove_note, remove_notegroup,
                               create_action, get_note, create_note)
from pytatki.views import type_id, has_access_to_usergroup


def test_user_has_access_to_note(insert_note):
    if has_access_to_note(1, 1) is not True:
        raise AssertionError()


def test_get_note(insert_note):
    if get_note(1, 1) != json.dumps({'idnote': 1, 'value': 'test', 'title': 'Test', 'status_id': 1, 'note_type': 'text', 'creator_id': 1, 'creator_login': 'test', 'notegroup_id': 1, 'notegroup_name': 'test'}):
        print(get_note(1, 1))
        raise AssertionError()


def test_type_id(insert_text_note_type):
    if 1 != type_id('text'):
        raise AssertionError()


def test_has_access_to_usergroup(insert_usergroup):
    if has_access_to_usergroup(1, 1) is not True:
        raise AssertionError()


def test_notegroup_empty(insert_notegroup, insert_usergroup):
    _, conn = connection()
    notegroup_id = insert_notegroup(conn, 'test_empty', insert_usergroup)
    if notegroup_empty(conn, notegroup_id) is not True:
        raise AssertionError()
    _.close()
    conn.close()


def test_remove_notegroup(insert_notegroup, insert_usergroup):
    _, conn = connection()
    conn.begin()
    notegroup_id = insert_notegroup(conn, 'test_remove', insert_usergroup)
    remove_notegroup(conn, notegroup_id)
    conn.commit()
    _.execute("SELECT * FROM notegroup WHERE idnotegroup = %s",
              pymysql.escape_string(str(notegroup_id)))
    notegroup = _.fetchone()
    if notegroup:
        print(notegroup)
        raise AssertionError()
    _.close()
    conn.close()


def test_note_exists(insert_note):
    _, conn = connection()
    if note_exists(idnote=1) is not True:
        raise AssertionError()
    _.close()
    conn.close()


def test_create_action(insert_user):
    _, conn = connection()
    _.execute("SELECT * FROM action WHERE content=\"create note Test\"")
    exists = _.fetchone()
    conn.close()
    if not exists:
        raise AssertionError()


def test_create_note(insert_user):
    con, conn = connection()
    note = create_note(conn, "test", "Test", 1, 1, 1, 1)
    conn.commit()
    if note:
        print(note)
        raise AssertionError()
    note = create_note(conn, "test_create_note", "TestCN", 1, 1, 1, 1)
    conn.commit()
    if note is None:
        print(note)
        raise AssertionError()
    con.close()
    conn.close()


def test_remove_note(insert_note):
    _, conn = connection()
    remove_note(conn, 1, 1)
    if note_exists(idnote=1) is not False:
        raise AssertionError()
    _.close()
    conn.close()


def test_has_access_to_notegroup(insert_notegroup):
    if has_access_to_notegroup(1, 1) != True:
        raise AssertionError()


def test_get_notegroup(insert_notegroup):
    if get_notegroup(1, 1) != json.dumps({'idnotegroup': 1, 'name': 'test', 'parent_id': 0}):
        print(get_notegroup(1, 1))
        raise AssertionError()
