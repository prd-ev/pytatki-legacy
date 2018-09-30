__author__ = "Patryk Niedźwiedziński"
"""Skrypt tworzenia bazy danych"""

from pytatki.dbconnect import connection
from pymysql import escape_string, connect
from passlib.hash import sha256_crypt
import configparser


def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts

create_database = parse_sql('sql/create-database.sql')
print(create_database)

def db_start():
    print("Connecting...")
    host = input("DB host: [127.0.0.1]")
    host = '127.0.0.1' if host == '' else host
    user = input("DB user: [root] ")
    user = 'root' if user == '' else user
    password = input("DB root password: ")
    conn = connect(host=host, user=user, password=password)
    print("Connection OK")
    print("Setting up database...")
    create_database = parse_sql('sql/create-database.sql')
    print(create_database)
    conn.begin()
    for query in create_database:
        conn.cursor().execute(query)
    conn.commit()
    conn.close()
    con, conn = connection()
    conn.begin()
    con.execute("INSERT INTO usergroup (name, description) VALUES (\"admins\", \"group of admins\")")
    admin_group_id = con.lastrowid
    con.execute("INSERT INTO status (name, description) VALUES (\"active\", \"Record is ative\")")
    active_id = con.lastrowid
    con.execute(
        "INSERT INTO status (name, description) VALUES (\"removed\", \"Record is removed\")")
    removed_id = con.lastrowid
    con.execute("INSERT INTO note_type (name, description) VALUES(\"file\", \"A file in format of txt, pdf, "
                "png, jpg, jpeg, gif, doc, docx, ppt, pptx, xslx, xsl, odt, rtf, cpp\")")
    file_id = con.lastrowid
    con.execute("INSERT INTO note_type (name, description) VALUES(\"text\", \"Just plain non-formated text\")")
    text_id = con.lastrowid
    con.execute("INSERT INTO note_type (name, description) VALUES(\"url\",\"An URL link to another resource\")")
    url_id = con.lastrowid
    username = input("Insert your admin login: ")
    email = input("Insert your admin email: ")
    password = input("Insert your admin password: ")
    con.execute("INSERT INTO user (login, password, email, status_id) VALUES (%s, %s, %s, %s)", (
        escape_string(username), escape_string(sha256_crypt.encrypt(str(password))), escape_string(email),
        escape_string(str(active_id))))
    admin_id = con.lastrowid
    con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)", (
        escape_string(str(admin_id)), escape_string(str(admin_group_id))))
    conn.commit()
    con.close()
    conn.close()
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    config['IDENTIFIERS']['ADMINGROUP_ID'] = admin_group_id
    config['IDENTIFIERS']['ADMIN_ID'] = admin_id
    config['IDENTIFIERS']['STATUS_ACTIVE_ID'] = active_id
    config['IDENTIFIERS']['STATUS_REMOVED_ID'] = removed_id
    config['IDENTIFIERS']['NOTE_TYPE_FILE_ID'] = file_id
    config['IDENTIFIERS']['NOTE_TYPE_TEXT_ID'] = text_id
    config['IDENTIFIERS']['NOTE_TYPE_URL_ID'] = url_id
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    db_start()
