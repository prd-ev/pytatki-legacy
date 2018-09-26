"""Widoki aplikacji"""
import os
import gc
from datetime import datetime
from sqlalchemy import func, and_
from flask import render_template, redirect, request, session, flash, send_file, g
from werkzeug.utils import secure_filename

from flask_login import logout_user, current_user
from main import APP
from config import CONFIG
from pytatki.models import User
from pytatki.view_manager import ban, login_manager, nocache
from pytatki import __version__
from dbconnect import connection
from pymysql import escape_string
import json

@APP.errorhandler(500)
def server_error_handler(error):
    return render_template("500.html"), 500

__author__ = 'Patryk Niedzwiedzinski'

ALLOWED_EXTENSIONS = set([
    'txt',
    'pdf',
    'png',
    'jpg',
    'jpeg',
    'gif',
    'doc',
    'docx',
    'ppt',
    'pptx',
    'xslx',
    'xsl',
    'odt',
    'rtf',
    'cpp',
    ])

def type_id(type_name):
    con, conn = connection()
    con.execute("SELECT idnote_type FROM note_type WHERE name = %s", escape_string(type_name))
    file_type = con.fetchone()
    con.close()
    conn.close()
    return file_type['idnote_type']

def has_access_to_notegroup(id_notegroup, id_user):
    """Returns true if user has access to notegroup, else false"""
    con, conn = connection()
    con.execute("SELECT iduser FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                (escape_string(str(id_user)), escape_string(str(id_notegroup))))
    returnValue =  con.fetchone()
    con.close()
    conn.close()
    if returnValue:
        return True
    False

def has_access_to_usergroup(id_usergroup, id_user):
    """Returns true if user has access to usergroup, else false"""
    con, conn = connection()
    con.execute("SELECT user_id FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                (escape_string(str(id_user)), escape_string(str(id_usergroup))))
    returnValue =  con.fetchone()
    con.close()
    conn.close()
    if returnValue:
        return True
    False

def find_notegroup_children(id_notegroup, id_user):
    """Generate dict with recurent children of usergroup"""
    if id_notegroup == 0 or not int(id_notegroup) or id_user == 0 or not int(id_user):
        return "ID must be a valid positive integer"
    children = []
    if has_access_to_notegroup(id_notegroup, id_user):
        con, conn = connection()
        con.execute("SELECT idnotegroup, folder_name FROM notegroup_view WHERE iduser = %s AND parent_id = %s", (escape_string(str(id_user)), escape_string(str(id_notegroup))))
        usergroups = con.fetchall()
        con.execute("SELECT idnote, value, note_type, creator_login, notegroup_id, notegroup_name, title AS 'name' FROM note_view WHERE notegroup_id = %s",
                    escape_string(str(id_notegroup)))
        notes = con.fetchall()
        con.close()
        conn.close()
        if usergroups:
            for usergroup in usergroups:
                children.append(usergroup)
        if notes:
            for note in notes:
                children.append(note)
    return json.dumps(children, ensure_ascii=False)


def has_access_to_note(id_note, id_user):
    """Check if user has access to note"""
    con, conn = connection()
    con.execute("SELECT notegroup_id FROM note WHERE idnote = %s",
                escape_string(str(id_note)))
    note = con.fetchone()
    con.execute("SELECT 1 FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                (escape_string(str(id_user)), escape_string(str(note['notegroup_id']))))
    has_access = con.fetchone()
    con.close()
    conn.close()
    if has_access:
        return True
    return False


def get_note(id_note, id_user):
    """Get note by id"""
    if has_access_to_note(id_note, id_user):
        con, conn = connection()
        con.execute("SELECT * FROM note_view WHERE idnote = %s",
                    escape_string(str(id_note)))
        note = con.fetchone()
        con.close()
        conn.close()
        return note

def get_root_id(id_usergroup, id_user):
    """Get if of root directory in usergroup"""
    if has_access_to_usergroup(id_usergroup, id_user):
        con, conn = connection()
        con.execute("SELECT idnotegroup FROM notegroup_view WHERE iduser = %s AND idusergroup = %s AND parent_id = 0", (escape_string(str(id_user)), escape_string(str(id_usergroup))))
        root_id = con.fetchone()
        if not root_id:
            return "No root folder" + str(id_user)
        root_id = root_id['idnotegroup']
        con.close()
        conn.close()
        return root_id
    return "Access denied"

def add_tag_to_note(tag, id_note, id_user):
    """Add tag to note, if tag doesn't exist create new"""
    if has_access_to_note(id_note, id_user):
        con, conn = connection()
        con.execute("SELECT * FROM tag WHERE name = %s", escape_string(tag))
        tag = con.fetchone()
        if not tag:
            conn.begin()
            con.execute("INSERT INTO tag (name) VALUES (%s)", escape_string(tag))
            tag_id = con.lastrowid
            conn.commit()
        else:
            tag_id = tag['idtag']
        conn.begin()
        con.execute("INSERT INTO tagging (note_id, tag_id) VALUES (%s, %s)",
                    (escape_string(str(id_note)), escape_string(str(tag_id))))
        conn.commit()
        con.execute("SELECT * FROM note_tags WHERE idnote = %s", escape_string(str(id_note)))
        note = con.fetchone()
        con.close()
        conn.close()
        return note

def postNote(title="xxd", type_name="text", value="xd", id_notegroup=1, id_user=1):
    """Post a note to database"""
    if not has_access_to_notegroup(id_notegroup, id_user):
        return "Access denied"
    if type_name == "file":
        return "File type is not supported via GraphQL"
    con, conn = connection()
    con.execute("SELECT idnote FROM note WHERE title = %s AND notegroup_id = %s", (escape_string(title), escape_string(str(id_notegroup))))
    used_name = con.fetchone()
    if used_name:
        con.close()
        conn.close()
        return "Cannot add note: used title"
    conn.begin()
    con.execute("INSERT INTO note (value, title, note_type_id, user_id, notegroup_id) VALUES (%s, %s, %s, %s, %s)", (escape_string(value), escape_string(title), escape_string(str(type_id(type_name))), escape_string(str(id_user)), escape_string(str(id_notegroup))))
    note_id = con.lastrowid
    con.execute("INSERT INTO action (content, user_id, note_id) VALUES (\"Create\", %s, %s)", (escape_string(str(id_user)), escape_string(str(note_id))))
    conn.commit()
    con.execute("SELECT * FROM note_view WHERE idnote = %s", escape_string(str(note_id)))
    note = con.fetchone()
    return note

@APP.route('/')
def homepage():
    if current_user.is_authenticated:
        return redirect('/app/')
    return render_template('landing_page.html')


@APP.route('/app/')
def app_view():
    if current_user.is_authenticated:
        content = find_notegroup_children(1, current_user['iduser'])
        #return jsonify(content)
        print(content)
        return render_template("homepage.html", subject=None, topics=None, notes=None, content=content)
    return redirect('/')

@APP.route('/about/')
def about():
    """About"""
    g.version = __version__
    return render_template('about.html')


@APP.route("/admin/")
@login_manager
def admin():
    """Admin"""
    if current_user.is_admin:
        return render_template('admin.html')
    flash("Nie mozesz tego zrobic", 'warning')
    return redirect('/')


@APP.route('/admin/delete/user/<int:identifier>/', methods=["GET"])
@login_manager
def delete_user(identifier):
    """Delete user"""
    if not User.query.filter_by(id=identifier).first().superuser:
        if identifier == current_user.id or current_user.admin:
            user = User.query.filter_by(id=identifier).first()
            if user:
                if identifier == current_user.id:
                    logout_user()
                    DB.session.delete(user)
                    DB.session.commit()
                    gc.collect()
                    session.clear()
                    gc.collect()
                    flash('Twoje konto zostalo usuniete', 'success')
                else:
                    DB.session.delete(user)
                    DB.session.commit()
                    flash('Uzytkownik zostal usuniety', 'success')
            else:
                flash('Nie ma takiego uzytkownika', 'warning')
    else:
        flash('Nie mozesz tego zrobic!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/note/<int:identifier>/', methods=["GET"])
@login_manager
def delete_note(identifier):
    """Delete note"""
    if current_user.is_admin:
        con, conn = connection()
        query = con.execute("SELECT * FROM note_view WHERE idnote = %s", escape_string(str(identifier)))
        note = con.fetchone()
        if query:
            con.execute("UPDATE note SET status_id = %s WHERE idnote = %s", (escape_string(str(CONFIG.json()['statuses']['removed_id'])), escape_string(str(identifier))))
            conn.commit()
            flash('Notatka zostala usunieta!', 'success')
        else:
            flash('Nie ma takiej notatki', 'warning')
    else:
        flash('Nie mozesz tego zrobic!', 'warning')
    con.close()
    conn.close()
    return redirect(request.args.get('next') if 'next' in request.args else '/')

@APP.route("/admin/user-list/")
@login_manager
def user_list():
    """wyswietla liste uzytkownikow"""
    if current_user.is_admin:
        con, conn = connection()
        con.execute("SELECT * FROM user")
        users_raw = con.fetchall()
        con.close()
        conn.close()
        users=[]
        for user_dict in users_raw:
            user = User()
            user.update(user_dict)
            users.append(user)
        return render_template('user_list.html', users=users)
    flash('Nie mozesz tego zrobic!', 'warning')
    return redirect('/')

@APP.route('/admin/give-admin/<int:identifier>/', methods=["GET"])
@login_manager
def give_admin(identifier):
    """Give admin"""
    con, conn = connection()
    con.execute("SELECT * FROM user WHERE iduser = %s", escape_string(identifier))
    user = con.fetchone()
    if current_user.is_admin and user and user['iduser'] != current_user:
        try:
            con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)", (escape_string(user['iduser']), CONFIG.json['admin_group_id']))
            conn.commit()
            flash('Przekazano uprawnienia administratora uzytkownikowi ' + str(
                user['login']), 'success')
        except Exception as error:
            flash("Blad: "+str(error), 'danger')
    return redirect(request.args.get('next') if 'next' in request.args else '/')

@APP.route('/admin/take-admin/<int:identifier>/', methods=["GET"])
@login_manager
def take_admin(identifier):
    """take admin"""
    if int(identifier) != int(CONFIG.json()['admin_id']):
        con, conn = connection()
        query = con.execute(
            "SELECT iduser, login FROM user WHERE iduser = %s", escape_string(identifier))
        user = con.fetchone()
        if current_user.is_admin and query:
            try:
                con.execute("DELETE FROM user_membership WHERE user_id = %s AND usergroup_id = %s", (escape_string(identifier), escape_string(int(CONFIG.json['admin_group_id']))))
                conn.commit()
                flash('Odebrano uprawnienia administratora uzytkownikowi ' + user['login'], 'success')
            except Exception as error:
                flash("Blad: " + str(error), 'danger')
        else:
            flash("Nie mozesz tego zrobic", 'warning')
        con.close()
        conn.close()
    else:
        flash("Nie mozesz tego zrobic", 'warning')
    return redirect(request.args.get('next') if 'next' in request.args else '/')

def allowed_file(filename):
    """Check if file has valid name and allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS \
           and not filename == ''

@APP.route('/add/', methods=["GET", "POST"])
@login_manager
def add():
    """Add new note"""
    if request.method == 'POST':
            form = request.form
            if 'file' not in request.files:
                flash('Blad: No file part', 'danger')
                return redirect(request.url)
            request_file = request.files['file']
            if request_file.filename == '':
                flash('Nie wybrano pliku', 'warning')
                return redirect(request.url)
            if request_file:
                if allowed_file(request_file.filename):
                    filename = secure_filename(request_file.filename)
                print(filename)
                if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['topic'], filename)):
                    if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['topic'])):
                        os.makedirs(os.path.join(APP.config['UPLOAD_FOLDER'], form['topic']))
                    request_file.save(os.path.join(APP.config['UPLOAD_FOLDER'], form['topic'], filename))
                else:
                    flash('Nieobslugiwane rozszerzenie', 'warning')
                    return redirect(request.url)
            con, conn = connection()
            con.execute("INSERT INTO note (value, title, note_type_id, user_id, usergroup_id, status_id) VALUES (%s, %s, %s, %s, %s, %s)",
                        (escape_string(str(os.path.join(form['topic'], filename))), escape_string(form['title']), escape_string(str(CONFIG.json()['note_types']['file_id'])), escape_string(str(current_user['iduser'])), escape_string(form['topic']), escape_string(str(CONFIG.json()['statuses']['active_id']))))
            conn.commit()
            note_id = con.lastrowid
            con.execute("INSERT INTO action (content, user_id, note_id, date) VALUES (\"Create note\", %s, %s, %s)", (escape_string(str(current_user['iduser'])), escape_string(str(note_id)), escape_string(str(datetime.now()))))
            conn.commit()
            con.close()
            conn.close()
            flash('Notatka zostala dodana!', 'success')
            return redirect(request.args.get('next') if 'next' in request.args else '/#'+str(form['topic']))
    else:
        con, conn = connection()
        con.execute("SELECT * FROM usergroup_membership a WHERE NOT EXISTS (SELECT * FROM usergroup_membership b WHERE b.parent_id = a.idusergroup) AND a.iduser = %s", escape_string(str(current_user['iduser'])))
        topics = con.fetchall()
        con.close()
        conn.close()
        return render_template('add.html', topics=topics)

@APP.route('/admin/add/', methods=["POST"])
@login_manager
def admin_add_post():
    """Admin add"""
    if current_user.is_admin:
            try:
                con, conn = connection()
                con.execute("SELECT idusergroup FROM usergroup WHERE lower(name) = lower(%s)", escape_string(request.form['title']))
                if con.fetchone():
                    flash("Dany przedmiot juz istnieje", 'warning')
                else:
                    print(request.form['parent_id'])
                    con.execute("SELECT idusergroup FROM usergroup_membership WHERE iduser = %s AND idusergroup = %s", (escape_string(str(current_user['iduser'])), escape_string(request.form['parent_id'])))
                    group = con.fetchone()
                    if group or request.form['parent_id']==0:
                        conn.begin()
                        con.execute("INSERT INTO usergroup (name, description, parent_id) VALUES (%s, %s, %s)", (escape_string(request.form['title']), escape_string(request.form['title']), escape_string(request.form['parent_id'] if 'parent_id' in request.form else 0)))
                        group_id = con.lastrowid
                        con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)", (escape_string(str(current_user['iduser'])), escape_string(str(group_id))))
                        conn.commit()
                        flash('Dodano przedmiot!', 'success')
                    else:
                        flash("Wystąpił błąd w zapytaniu", 'warning')
                con.close()
                conn.close()
            except Exception as e:
                flash('Blad: '+str(e), 'danger')
    else:
        flash('Nie mozesz tego zrobic', 'warning')
    return redirect(request.args.get('next') if 'next' in request.args else '/')

@APP.route('/admin/add/', methods=["GET"])
@login_manager
def admin_add_get():
    """Admin add"""
    if current_user.is_admin:
        con, conn = connection()
        con.execute("SELECT idusergroup, name, parent_id FROM usergroup_membership WHERE iduser = %s", escape_string(str(current_user['iduser'])))
        subjects = con.fetchall()
        con.close()
        conn.close()
        return render_template('admin_add.html', subjects=subjects)
    else:
        flash("Nie masz uprawnien", 'warning')
    return redirect(request.args.get('next') if 'next' in request.args else '/')

@APP.route('/download/<identifier>/')
@login_manager
@nocache
def download(identifier):
    """Download file"""
    if current_user.is_authenticated:
        if has_access_to_note(identifier, current_user['iduser']):
            con, conn = connection()
            con.execute("SELECT * FROM note_view WHERE idnote = %s", escape_string(identifier))
            note = con.fetchone()
            if note['note_type'] == "file":
                return send_file(os.path.join(APP.config['UPLOAD_FOLDER'], note['value']))
            else:
                return note['value']
    flash("Musisz byc zalogowany", 'warning')
    return redirect('/')

@APP.route('/notatki/')
def react():
	return render_template('index.html')

@APP.route('/graphql/')
def graphql_explorer():
    return render_template("graphql.html")

APP.secret_key = CONFIG.secret_key
