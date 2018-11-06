import json

import pymysql
from passlib.hash import sha256_crypt

from pytatki.config import parse_config

__author__ = "Filip Wachowiak & Patryk Niedzwiedzinski"

CONFIG = parse_config('config.json', check_db_configuration=False)


def connection(host=CONFIG['DATABASE']['DB_HOST'], user=CONFIG['DATABASE']['DB_USER'],
               password=CONFIG['DATABASE']['DB_PASSWORD'], db=CONFIG['DATABASE']['DB_NAME'],
               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db,
                           charset=charset,
                           cursorclass=cursorclass)
    c = conn.cursor()
    return c, conn


def create_usergroup(conn, name, description, parent_id='0'):
    """Insert usergroup into the database using given connection and returns its id"""
    c = conn.cursor()
    c.execute(
        "INSERT INTO usergroup (name, description) VALUES (%s, %s)", (pymysql.escape_string(name), pymysql.escape_string(description)))
    return c.lastrowid


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
    return True if con.fetchone() else False


def create_action(conn, content, iduser, idnote):
    conn.cursor().execute(
        "INSERT INTO action (content, note_id, user_id) VALUES (%s, %s, %s)",
        (
            pymysql.escape_string(content),
            pymysql.escape_string(str(idnote)),
            pymysql.escape_string(str(iduser))
        )
    )


def remove_note(conn, idnote, iduser):
    """Removes a note"""
    if has_access_to_note(idnote, iduser):
        conn.cursor().execute(
            "UPDATE note SET status_id = %s WHERE idnote = %s",
            (pymysql.escape_string(str(
                CONFIG['IDENTIFIERS']['status_removed_id'])), pymysql.escape_string(str(idnote)))
        )
        create_action(conn, 'removes a note \'{}\''.format(
            str(idnote)), iduser, idnote)
    return json.dumps({"data": "no permission"})


def add_user_to_usergroup(conn, iduser, idusergroup):
    """Add user to usergroup"""
    c = conn.cursor()
    c.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)",
              (pymysql.escape_string(str(iduser)), pymysql.escape_string(str(idusergroup))))
    return c.lastrowid


def create_notegroup(conn, name, idusergroup, parent_id='0'):
    """Insert new notegroup into the database in given usergroup using given connection and returns its id"""
    c = conn.cursor()
    c.execute("INSERT INTO notegroup (name, parent_id) VALUES (%s, %s)",
              (pymysql.escape_string(name), pymysql.escape_string(str(parent_id))))
    idnotegroup = c.lastrowid
    c.execute("INSERT INTO usergroup_has_notegroup (usergroup_id, notegroup_id) VALUES (%s, %s)",
              (pymysql.escape_string(str(idusergroup)), pymysql.escape_string(str(idnotegroup))))
    return idnotegroup


def notegroup_empty(conn, idnotegroup):
    """Checks if notegroup is empty"""
    not_empty = conn.cursor().execute(
        "SELECT * FROM note WHERE notegroup_id = %s AND status_id = 1", pymysql.escape_string(str(idnotegroup)))
    return False if not_empty else True


def remove_notegroup(conn, idnotegroup):
    """Important function"""
    if notegroup_empty(conn, idnotegroup):
        print("x")
        c = conn.cursor()
        c.execute("DELETE FROM usergroup_has_notegroup WHERE notegroup_id = %s",
                  pymysql.escape_string(str(idnotegroup)))
        c.execute("DELETE FROM notegroup WHERE idnotegroup = %s",
                  pymysql.escape_string(str(idnotegroup)))
        return True
    return False


def create_status(conn, name, description):
    """Insert status into the database using given connection and returns its id"""
    c = conn.cursor()
    c.execute(
        "INSERT INTO status (name, description) VALUES (%s, %s)", (pymysql.escape_string(name), pymysql.escape_string(description)))
    return c.lastrowid


def create_note_type(conn, name, description):
    """Insert note type into the database using given connection and returns its id"""
    c = conn.cursor()
    c.execute("INSERT INTO note_type (name, description) VALUES(%s, %s)",
              (pymysql.escape_string(name), pymysql.escape_string(description)))
    return c.lastrowid


def create_user(conn, login, password, email, status_id):
    """Insert user into the database using given connection and returns its id"""
    c = conn.cursor()
    c.execute("INSERT INTO user (login, password, email, status_id) VALUES (%s, %s, %s, %s)", (
        pymysql.escape_string(login), pymysql.escape_string(
            sha256_crypt.encrypt(str(password))), pymysql.escape_string(email),
        pymysql.escape_string(str(status_id))))
    return c.lastrowid


def create_note(conn, value, title, note_type_id, user_id, notegroup_id, status_id):
    if not note_exists(title=title, notegroup_id=notegroup_id):
        c = conn.cursor()
        c.execute(
            "INSERT INTO note (value, title, note_type_id, user_id, notegroup_id, status_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                pymysql.escape_string(value),
                pymysql.escape_string(title),
                pymysql.escape_string(str(note_type_id)),
                pymysql.escape_string(str(user_id)),
                pymysql.escape_string(str(notegroup_id)),
                pymysql.escape_string(str(status_id))
            )
        )
        idnote = c.lastrowid
        create_action(conn, "create note {}".format(title), user_id, idnote)
        return idnote
    return None


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


def remove_user(conn, iduser):
    """Removes user from database"""
    conn.cursor().execute("DELETE FROM user WHERE iduser = %s",
                          pymysql.escape_string(str(iduser)))
    # TODO: other tables


def has_access_to_notegroup(id_notegroup, id_user):
    """Returns true if user has access to notegroup, else false"""
    con, conn = connection()
    con.execute("SELECT iduser FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                (pymysql.escape_string(str(id_user)), pymysql.escape_string(str(id_notegroup))))
    return_value = con.fetchone()
    con.close()
    conn.close()
    return True if return_value else False


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
