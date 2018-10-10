from pytatki.dbconnect import connection, create_status, create_usergroup, add_user_to_usergroup, create_notegroup, create_note_type, create_note, notegroup_empty, remove_notegroup
from pytatki.views import has_access_to_note, type_id, has_access_to_usergroup
from init_db import db_init

def test_user_has_access_to_note(insert_note):
    if has_access_to_note(1, 1) != True:
        raise AssertionError()

def test_type_id(insert_text_note_type):
    if 1 != type_id('text'):
        raise AssertionError()

def test_has_access_to_usergroup(insert_usergroup):
    if has_access_to_usergroup(1, 1) != True:
        raise AssertionError()

def test_notegroup_empty(insert_notegroup, insert_usergroup):
    _, conn = connection()
    notegroup_id = insert_notegroup(conn, 'test_empty', insert_usergroup)
    if notegroup_empty(conn, notegroup_id) != True:
        raise AssertionError()
