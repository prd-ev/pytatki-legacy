import flask_mail
from pytatki.user import send_confirmation_email
from pymysql import escape_string
from pytatki.dbconnect import connection
from pytatki.main import APP


@APP.route('/admin/verify_all/')
def send_to_all():
    con, conn = connection()
    con.execute("SELECT email FROM user WHERE email_confirm = 0")
    emails = [email['email'] for email in con.fetchall()]
    con.close()
    conn.close()

    for email in emails:
        send_confirmation_email(email)
    return "success"
