from pytatki.dbconnect import (create_usergroup, add_user_to_usergroup,
                               connection, create_notegroup)
import json


def api_create_usergroup(name, description, iduser):
    con, conn = connection()
    conn.begin()
    idusergroup = create_usergroup(conn, name, description)
    add_user_to_usergroup(conn, iduser, idusergroup)
    create_notegroup(conn, "root{}".format(name), idusergroup)
    conn.commit()
    con.close()
    conn.close()
    return json.dumps({'data': idusergroup})


def api_create_notegroup(name, idusergroup, parent_id, id_user):
    con, conn = connection()
    conn.begin()
    idnotegroup = create_notegroup(
        conn, name, idusergroup, parent_id=parent_id)
    conn.commit()
    con.close()
    conn.close()
    return json.dumps({'data': idnotegroup})
