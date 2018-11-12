"""Get functions"""
import pymysql
import json
from pytatki.config import parse_config
from pytatki.dbconnect.main import connection
from pytatki.dbconnect.checks import has_access_to_note, has_access_to_notegroup, has_access_to_usergroup

__author__ = "Patryk Niedźwiedziński"

CONFIG = parse_config('config.json', check_db_configuration=False)


def get_type_id(type_name):
    con, conn = connection()
    con.execute("SELECT idnote_type FROM note_type WHERE name = %s",
                pymysql.escape_string(type_name))
    file_type = con.fetchone()
    con.close()
    conn.close()
    return file_type['idnote_type']


def get_usergroups_of_user(iduser):
    """Get list of usergroups"""
    con, conn = connection()
    con.execute("SELECT idusergroup, name, color, description, image_path FROM usergroup_membership WHERE iduser = %s",
                pymysql.escape_string(str(iduser)))
    usergroups = con.fetchall()
    con.close()
    conn.close()
    return json.dumps(usergroups, ensure_ascii=False)


def get_users_of_usergroup(idusergroup, iduser):
    """Get list of users of usergroup"""
    if has_access_to_usergroup(idusergroup, iduser):
        con, conn = connection()
        con.execute("SELECT iduser, login FROM usergroup_membership WHERE idusergroup = %s",
                    pymysql.escape_string(str(idusergroup)))
        users = con.fetchall()
        con.close()
        conn.close()
        return json.dumps(users)
    return None


def get_root_id(id_usergroup, id_user):
    """Get if of root directory in usergroup"""
    if has_access_to_usergroup(id_usergroup, id_user):
        con, conn = connection()
        con.execute("SELECT idnotegroup FROM notegroup_view WHERE iduser = %s AND idusergroup = %s AND parent_id = 0",
                    (pymysql.escape_string(str(id_user)), pymysql.escape_string(str(id_usergroup))))
        root_id = con.fetchone()
        if not root_id:
            return "No root folder" + str(id_user)
        root_id = root_id['idnotegroup']
        con.close()
        conn.close()
        return root_id
    return "Access denied"


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
