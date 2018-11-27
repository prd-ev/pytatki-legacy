from pytatki.views import get_usergroups_of_user
from pytatki.dbconnect import connection, remove_user
from pymysql import escape_string


def test_get_usergroups_of_user(insert_usergroup):
    if str(get_usergroups_of_user(1)) != '[{"idusergroup": 1, "name": "test", "color": "#ffffff", "description": "test", "image_path": "img/default.jpg"}]':
        raise AssertionError()


def test_remove_user(insert_user_new):
    con, conn = connection()
    user_id = insert_user_new(conn, "delete_me", "delete", "delete@me", 1)
    conn.commit()
    con.execute("SELECT * FROM user WHERE iduser = %s",
                escape_string(str(user_id)))
    user_exists = con.fetchone()
    if not user_exists:
        raise AssertionError()
    remove_user(conn, user_id)
    conn.commit()
    con.execute("SELECT * FROM user WHERE iduser = %s",
                escape_string(str(user_id)))
    user_exists = con.fetchone()
    if user_exists:
        raise AssertionError()
    con.close()
    conn.close()


# TODO: test pytatki.dbconnect.remove_user
