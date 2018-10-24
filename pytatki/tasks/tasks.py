from pytatki.main import CELERY
import schedule
import time
from datetime import datetime, timedelta
from pytatki.dbconnect import connection
from pymysql import escape_string


@CELERY.task(name='tasks.remove_bin')
def remove_bin(notegroup=None):
    """TASK - Removes permanently deleted notes that are for 30 days in trash"""
    con, conn = connection()
    date = datetime.today() - timedelta(days=30)
    sql = "SELECT note_id FROM action WHERE content LIKE 'removes a note %%' AND date <= %s"
    args = escape_string(date.strftime("%Y-%m-%d"))
    if notegroup:
        sql += " AND note_id IN (SELECT idnote FROM note WHERE status_id = 2 AND notegroup_id = %s)"
        args = (args, escape_string(str(notegroup)))
    con.execute(sql, args)
    notes_to_delete = con.fetchall()
    for note in notes_to_delete:
        conn.begin()
        con.execute("DELETE FROM action WHERE note_id = %s",
                    escape_string(str(note['note_id'])))
        con.execute("DELETE FROM tagging WHERE note_id = %s",
                    escape_string(str(note['note_id'])))
        con.execute("DELETE FROM note WHERE idnote = %s",
                    escape_string(str(note['note_id'])))
        conn.commit()
    con.close()
    conn.close()

schedule.every().day.at("10:30").do(remove_bin)

@CELERY.task(name='tasks.run_jobs')
def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)
