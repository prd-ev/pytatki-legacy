"""Get functions"""
import pymysql
import json
from pytatki.config import parse_config
from pytatki.dbconnect.main import connection
from pytatki.dbconnect.checks import has_access_to_note, has_access_to_notegroup

__author__ = "Patryk Niedźwiedziński"

CONFIG = parse_config('config.json', check_db_configuration=False)


def get_note(id_note, id_user):
    """Get note by id"""
    if has_access_to_note(id_note, id_user):
        con, conn = connection()
        con.execute("SELECT * FROM note_view WHERE idnote = %s",
                    pymysql.escape_string(str(id_note)))
        note = con.fetchone()
        con.close()
        conn.close()
        return json.dumps(note)
    return False


def get_notegroup(idnotegroup, iduser):
    """Get info about notegroup"""
    if has_access_to_notegroup(idnotegroup, iduser):
        con, conn = connection()
        con.execute("SELECT * FROM notegroup WHERE idnotegroup = %s",
                    pymysql.escape_string(str(idnotegroup)))
        notegroup_info = con.fetchone()
        con.close()
        conn.close()
        return json.dumps(notegroup_info)
    return False


def get_last_note_actions(idnote, iduser):
    """Get 5 last actions of note"""
    con, conn = connection()
    con.execute("SELECT * FROM action WHERE note_id = %s ORDER BY date DESC",
                pymysql.escape_string(str(idnote)))
    last_actions = con.fetchmany(5)
    last_actions = [
        {
            'idaction': row['idaction'], 'content': row['content'], 'user_id': row['user_id'], 'date': row['date'].strftime('%I:%M %d.%m.%Y')
        }
        for row in last_actions
    ]
    con.close()
    conn.close()
    print(last_actions)
    return json.dumps(last_actions)
