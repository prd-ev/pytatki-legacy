"""Remove functions"""
import pymysql
import json
from pytatki.config import parse_config
from pytatki.dbconnect.checks import has_access_to_note, notegroup_empty
from pytatki.dbconnect.create import create_action

__author__ = "Patryk Niedźwiedziński"


CONFIG = parse_config('config.json', check_db_configuration=False)


def remove_note(conn, idnote, iduser):
    """Removes a note"""
    if has_access_to_note(idnote, iduser):
        print("has")
        conn.cursor().execute(
            "UPDATE note SET status_id = %s WHERE idnote = %s",
            (pymysql.escape_string(str(
                CONFIG['IDENTIFIERS']['status_removed_id'])), pymysql.escape_string(str(idnote)))
        )
        create_action(conn, 'removes a note \'{}\''.format(
            str(idnote)), iduser, idnote)
        return json.dumps({'data': 'success'})
    return json.dumps({"data": "no permission"})


def remove_notegroup(conn, idnotegroup):
    """Important function"""
    if notegroup_empty(idnotegroup):
        c = conn.cursor()
        c.execute("DELETE FROM usergroup_has_notegroup WHERE notegroup_id = %s",
                  pymysql.escape_string(str(idnotegroup)))
        c.execute("DELETE FROM notegroup WHERE idnotegroup = %s",
                  pymysql.escape_string(str(idnotegroup)))
        return True
    return False


def remove_user(conn, iduser):
    """Removes user from database"""
    conn.cursor().execute("DELETE FROM user WHERE iduser = %s",
                          pymysql.escape_string(str(iduser)))
    # TODO: other tables
