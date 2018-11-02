__author__ = "Patryk Niedźwiedziński"
"""Skrypt tworzenia bazy danych"""

from pymysql import escape_string, connect
from pytatki.dbconnect import connection, create_usergroup, create_status, create_note_type, create_user
import json


def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for _, line in enumerate(data):
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
    with open('config.json', 'r') as fp:
        config = json.load(fp)
    config['IDENTIFIERS']['admingroup_id'] = config_dict['admingroup_id']
    config['IDENTIFIERS']['admin_id'] = config_dict['admin_id']
    config['IDENTIFIERS']['status_active_id'] = config_dict['active_id']
    config['IDENTIFIERS']['status_removed_id'] = config_dict['removed_id']
    config['IDENTIFIERS']['note_type_file_id'] = config_dict['file_id']
    config['IDENTIFIERS']['note_type_text_id'] = config_dict['text_id']
    config['IDENTIFIERS']['note_type_url_id'] = config_dict['url_id']
    with open('config.json', 'w') as configfile:
        configfile.truncate(0)
        json.dump(config, configfile)


def db_init(host=None, user=None, password=None):
    """Create database from sql/create-database"""
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
    con, conn = connection(host='127.0.0.1', user='pytatki',
                           password='pytatki', db='pytatki')
    conn.begin()
    admin_group_id = create_usergroup(conn, 'admins', 'Group of admins')
    active_id = create_status(conn, 'active', 'Record is active')
    removed_id = create_status(conn, 'removed', 'Record is removed')
    file_id = create_note_type(
        conn, "file", "A file in format of txt, pdf, png, jpg, jpeg, gif, doc, docx, ppt, pptx, xslx, xsl, odt, rtf, cpp")
    text_id = create_note_type(conn, "text", "Just plain non-formated text")
    url_id = create_note_type(conn, "url", "An URL link to another resource")
    username = input("Insert your admin login: [admin]")
    username = 'admin' if username == '' else username
    email = input("Insert your admin email: ")
    password = input("Insert your admin password: ")
    admin_id = create_user(conn, username, password, email, active_id)
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
