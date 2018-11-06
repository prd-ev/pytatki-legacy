from pytatki.dbconnect import create_usergroup, add_user_to_usergroup, connection
import json


def api_create_usergroup(name, description, iduser):
    con, conn = connection()
    conn.begin()
    idusergroup = create_usergroup(conn, name, description)
    add_user_to_usergroup(conn, iduser, idusergroup)
    conn.commit()
    con.close()
    conn.close()
    return json.dumps({'data': idusergroup})
