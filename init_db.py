__author__ = "Patryk Niedźwiedziński"
"""Skrypt tworzenia bazy danych"""

from dbconnect import connection
from pymysql import escape_string
from passlib.hash import sha256_crypt
import json

def db_start():
    error = "There was an error while setting up database"
    print("Connecting...")
    con, conn = connection()
    print("Connection OK")
    print("Setting up database...")
    query = con.execute("INSERT INTO usergroup (name, description) VALUES (\"admins\", \"group of admins\")")
    if not query == 0:
        conn.commit()
        admin_group_id = con.lastrowid
        query = con.execute("INSERT INTO status (name, description) VALUES (\"active\", \"Record is ative\")")
        if not query == 0:
            conn.commit()
            active_id = con.lastrowid
            con.execute(
                "INSERT INTO status (name, description) VALUES (\"removed\", \"Record is removed\")")
            conn.commit()
            removed_id = con.lastrowid
            con.execute("INSERT INTO note_type (name, description) VALUES(\"file\", \"A file in format of txt, pdf, png, jpg, jpeg, gif, doc, docx, ppt, pptx, xslx, xsl, odt, rtf, cpp\")")
            conn.commit()
            file_id = con.lastrowid
            con.execute("INSERT INTO note_type (name, description) VALUES(\"text\", \"Just plain non-formated text\")")
            conn.commit()
            text_id = con.lastrowid
            con.execute("INSERT INTO note_type (name, description) VALUES(\"url\", \"An URL link to another resource\")")
            conn.commit()
            url_id = con.lastrowid
            username = input("Insert your admin login: ")
            email = input("Insert your admin email: ")
            password = input("Insert your admin password: ")
            con.execute("INSERT INTO user (login, password, email, status_id) VALUES (%s, %s, %s, %s)", (escape_string(username), escape_string(sha256_crypt.encrypt(str(password))), escape_string(email), escape_string(str(active_id))))
            conn.commit()
            admin_id = con.lastrowid
            con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)", (escape_string(str(admin_id)), escape_string(str(admin_group_id))))
            conn.commit()
            else:
                print(error)
        else:
            print(error)
    else:
        print(error)
    con.close()
    conn.close()
    with open("config/config.json", "r+") as f:
        json.dump({'admin_group_id': admin_group_id, 'admin_id': admin_id, 'statuses': {'active_id': active_id, 'removed_id': removed_id}, 'note_types': {'file_id': file_id, 'text_id': text_id, 'url_id': url_id}}, f)


if __name__ == '__main__':
    db_start()
