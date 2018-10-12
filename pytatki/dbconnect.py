import pymysql
from pytatki.config import parse_config
from passlib.hash import sha256_crypt

__author__ = "Filip Wachowiak & Patryk Niedzwiedzinski"

CONFIG = parse_config('config.ini', check_db_configuration=False)


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


def note_exists(conn, idnote):
    """Checks if note exists"""
    #TODO: is active!
    note_exists = conn.cursor().execute(
        "SELECT * FROM note_view WHERE idnote = %s", pymysql.escape_string(str(idnote)))
    return True if note_exists else False

def create_action(conn, content, iduser, idnote):
    #TODO: add action
    pass

def remove_note(conn, idnote):
    """Removes a note"""
    #TODO: move to note-history
    conn.cursor().execute("UPDATE note SET status_id = %s WHERE idnote = %s",
                          (pymysql.escape_string(str(CONFIG['IDENTIFIERS']['STATUS_REMOVED_ID'])), pymysql.escape_string(str(idnote))))
    #TODO: action about remove


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
    #TODO: removed notes
    """Chcecks if notegroup is empty"""
    not_empty = conn.cursor().execute(
        "SELECT * FROM note WHERE notegroup_id = %s", pymysql.escape_string(str(idnotegroup)))
    return False if not_empty else True


def remove_notegroup(conn, idnotegroup):
    """Important function"""
    if notegroup_empty(conn, idnotegroup):
        print("x")
        c = conn.cursor()
        c.execute("DELETE FROM usergroup_has_notegroup WHERE notegroup_id = %s", pymysql.escape_string(str(idnotegroup)))
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
    return c.lastrowid
