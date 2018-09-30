from src.api.v1.auth import auth
from pytatki.main import APP
from flask import send_from_directory
from pytatki.dbconnect import connection
from pymysql import escape_string

@APP.route('/api/note/<identifier>/', methods=["GET"])
@APP.route('/api/note/<identifier>', methods=["GET"])
@auth.login_required
def api_get_note_by_id(identifier):
    con, conn = connection()
    con.execute("SELECT * FROM note_view WHERE idnote = %s", escape_string(identifier))
    note = con.fetchone()
    return send_from_directory(APP.config['UPLOAD_FOLDER'], note['value'])