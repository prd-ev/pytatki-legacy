from pytatki.main import CELERY, APP
import schedule
import time
import os
from datetime import datetime, timedelta
from pytatki.dbconnect import connection
from pytatki.views import has_access_to_notegroup
from pymysql import escape_string


@CELERY.task(name='tasks.remove_bin')
def remove_bin(iduser, notegroup=None):
    """TASK - Removes permanently deleted notes that are for 30 days in trash"""
    con, conn = connection()
    date = datetime.today() - timedelta(days=30)
    sql = "SELECT note_id FROM action WHERE content LIKE 'removes a note %%' AND date <= %s"
    args = escape_string(date.strftime("%Y-%m-%d"))
    if notegroup:
        if has_access_to_notegroup(notegroup, iduser):
            sql += " AND note_id IN (SELECT idnote FROM note WHERE status_id = 2 AND notegroup_id = %s)"
            args = (args, escape_string(str(notegroup)))
        else:
            raise ConnectionRefusedError("Invalid notegroup or user")
    con.execute(sql, args)
    notes_to_delete = con.fetchall()
    for note in notes_to_delete:
        con.execute("SELECT * FROM note WHERE idnote = %s", escape_string(str(note['note_id'])))
        note = con.fetchone()
        conn.begin()
        con.execute("DELETE FROM action WHERE note_id = %s",
                    escape_string(str(note['note_id'])))
        con.execute("DELETE FROM tagging WHERE note_id = %s",
                    escape_string(str(note['note_id'])))
        con.execute("DELETE FROM note WHERE idnote = %s",
                    escape_string(str(note['note_id'])))
        conn.commit()
        if note['note_type_id'] == 1:
            #TODO: file id
            path = os.path.join(APP.config['UPLOAD_FOLDER'], note['notegroup_id'], note['content'])
            if os.path.exists(path):
                os.remove(path)
    con.close()
    conn.close()

@CELERY.task(name='tasks.email_notification')
def email_not_verified(usergroup_id):
    """TASK - Send email to users in usergroup when someone adds new note"""
    con, conn = connection()
    pass

schedule.every().day.at("10:30").do(remove_bin)

@CELERY.task(name='tasks.run_jobs')
def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)
