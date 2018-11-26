"""Checks"""
import pymysql
from pytatki.dbconnect.main import connection

__author__ = "Patryk Niedźwiedziński"


def has_access_to_usergroup(id_usergroup, id_user):
    """Returns true if user has access to usergroup, else false"""
    con, conn = connection()
    con.execute("SELECT user_id FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                (pymysql.escape_string(str(id_user)), pymysql.escape_string(str(id_usergroup))))
    return_value = con.fetchone()
    con.close()
    conn.close()
    return True if return_value else False


def has_access_to_note(id_note, id_user):
    """Check if user has access to note"""
    if note_exists(idnote=id_note):
        con, conn = connection()
        con.execute("SELECT notegroup_id FROM note WHERE idnote = %s",
                    pymysql.escape_string(str(id_note)))
        note = con.fetchone()
        con.execute("SELECT 1 FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                    (pymysql.escape_string(str(id_user)), pymysql.escape_string(str(note['notegroup_id']))))
        has_access = con.fetchone()
        con.close()
        conn.close()
        if has_access:
            return True
    return False


def note_exists(idnote=None, title=None, notegroup_id=None):
    """Checks if note exists"""
    con, conn = connection()
    sql = "SELECT * FROM note WHERE {} AND status_id = 1"
    args = (pymysql.escape_string(str(idnote)))
    if idnote:
        sql = sql.format("idnote= %s")
    elif title and notegroup_id:
        sql = sql.format("title = %s AND notegroup_id = %s")
        args = (pymysql.escape_string(title),
                pymysql.escape_string(str(notegroup_id)))
    else:
        return None
    con.execute(sql, args)
    note_exists = con.fetchone()
    con.close()
    conn.close()
    return True if note_exists else False


def notegroup_empty(idnotegroup):
    """Checks if notegroup is empty"""
    con, conn = connection()
    con.execute(
        "SELECT * FROM note WHERE notegroup_id = %s AND status_id = 1", pymysql.escape_string(str(idnotegroup)))
    not_empty = con.fetchone()
    con.close()
    conn.close()
    return False if not_empty else True


def has_access_to_notegroup(id_notegroup, id_user):
    """Returns true if user has access to notegroup, else false"""
    con, conn = connection()
    con.execute("SELECT iduser FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                (pymysql.escape_string(str(id_user)), pymysql.escape_string(str(id_notegroup))))
    return_value = con.fetchone()
    con.close()
    conn.close()
    return True if return_value else False
