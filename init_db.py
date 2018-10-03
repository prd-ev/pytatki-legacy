__author__ = "Patryk Niedźwiedziński"
"""Skrypt tworzenia bazy danych"""

import configparser
from pymysql import escape_string, connect
from passlib.hash import sha256_crypt
from pytatki.dbconnect import connection, create_usergroup, create_status

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

def save_to_config(config_dict):
    """
    Save data to config.ini
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    config.add_section('IDENTIFIERS')
    config['IDENTIFIERS']['ADMINGROUP_ID'] = str(config_dict['admingroup_id'])
    config['IDENTIFIERS']['ADMIN_ID'] = str(config_dict['admin_id'])
    config['IDENTIFIERS']['STATUS_ACTIVE_ID'] = str(config_dict['active_id'])
    config['IDENTIFIERS']['STATUS_REMOVED_ID'] = str(config_dict['removed_id'])
    config['IDENTIFIERS']['NOTE_TYPE_FILE_ID'] = str(config_dict['file_id'])
    config['IDENTIFIERS']['NOTE_TYPE_TEXT_ID'] = str(config_dict['text_id'])
    config['IDENTIFIERS']['NOTE_TYPE_URL_ID'] = str(config_dict['url_id'])
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def db_init(host=None, user=None, password=None):
    """""Create database from sql/create-database"""
    
    host = input("DB host: [127.0.0.1]") if not host else host
    host = '127.0.0.1' if host == '' else host
    user = input("DB user: [root] ") if not user else user
    user = 'root' if user == '' else user
    password = input("DB root password: ") if not password else password
    print("Connecting...")
    conn = connect(host=host, user=user, password=password)
    print("Connection OK")
    print("Setting up database...")
    create_database = parse_sql('sql/create-database.sql')
    conn.begin()
    for query in create_database:
        conn.cursor().execute(query)
    conn.commit()
    conn.close()
    con, conn = connection(host='127.0.0.1', user='pytatki', password='pytatki', db='pytatki')
    conn.begin()
    admin_group_id = create_usergroup(conn, 'admins', 'Group of admins')
    active_id = create_status(conn, 'active', 'Record is active')
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
    username = input("Insert your admin login: [admin]")
    username = 'admin' if username == '' else username
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
    save_to_config({
        'admingroup_id': admin_group_id,
        'admin_id': admin_id,
        'active_id': active_id,
        'removed_id': removed_id,
        'file_id': file_id,
        'text_id': text_id,
        'url_id': url_id
        })


if __name__ == '__main__':
    db_init()
