"""Widoki aplikacji"""
import os
import gc
from datetime import datetime
from sqlalchemy import func, and_
from flask import render_template, redirect, request, session, flash, send_file, g, jsonify
from werkzeug.utils import secure_filename

from flask_login import logout_user, current_user
from main import APP
from config import CONFIG
from pytatki.models import User
from pytatki.view_manager import ban, login_manager, nocache
from pytatki import __version__
from dbconnect import connection
from pymysql import escape_string


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

def find_usergroup_children(id_usergroup, id_user):
    """Generate dict with recurent children of usergroup"""
    con, conn = connection()
    con.execute("SELECT user_id FROM user_membership WHERE user_id = %s AND usergroup_id = %s", (escape_string(str(id_user)), escape_string(str(id_usergroup))))
    user_in_group = con.fetchone()
    con.close()
    conn.close()
    childrens = []
    if user_in_group:
        con, conn = connection()
        con.execute("SELECT idusergroup, name, color, description, image_path FROM usergroup_membership WHERE iduser = %s AND parent_id = %s", (escape_string(str(id_user)), escape_string(str(id_usergroup))))
        usergroups = con.fetchall()
        con.execute("SELECT * FROM note_view WHERE parent_id = %s",
                    escape_string(str(id_usergroup)))
        notes = con.fetchall()
        con.close()
        conn.close()
        if usergroups:
            for usergroup in usergroups:
                usergroup.update(find_usergroup_children(
                    usergroup['idusergroup'], id_user))
                childrens.append(usergroup)
        if notes:
            for note in notes:
                childrens.append(note)
    return dict({"childrens": childrens})

@APP.route('/')
@ban
def homepage():
    """Homepage"""
    if current_user.is_authenticated:
        #return jsonify(find_usergroup_children(1, current_user['iduser']))
        return render_template('homepage.html')
    return render_template('homepage.html')


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
        query = con.execute("SELECT * FROM note_view WHERE idnote = %s", escape_string(identifier))
        note = con.fetchone()
        if query:
            con.execute("UPDATE note SET status_id = %s WHERE idnote = %s", (escape_string(int(CONFIG.json()['statuses']['removed_id'])), escape_string(identifier)))
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
        try:
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
        except Exception as error:
            flash("Blad: " + str(error), 'danger')
            return redirect(request.args.get('next') if 'next' in request.args else '/')
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
                        con.execute("INSERT INTO usergroup (name, description, parent_id) VALUES (%s, %s, %s)", (escape_string(request.form['title']), escape_string(request.form['title']), escape_string(request.form['parent_id'] if 'parent_id' in request.form else 0)))
                        conn.commit()
                        con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)", (escape_string(str(current_user['iduser'])), escape_string(str(con.lastrowid))))
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
        return render_template('admin_add.html', subjects=subjects)
    else:
        flash("Nie masz uprawnien", 'warning')
    return redirect(request.args.get('next') if 'next' in request.args else '/')

def has_access_to_note(id_note, id_user):
    """Check if user has access to note"""
    con, conn = connection()
    con.execute("SELECT usergroup_id FROM note WHERE idnote = %s", escape_string(str(id_note)))
    note = con.fetchone()
    con.execute("SELECT 1 FROM user_membership WHERE user_id = %s AND usergroup_id = %s", (escape_string(str(id_user)), escape_string(str(note['usergroup_id']))))
    if con.fetchone():
        return True
    return False

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

APP.secret_key = CONFIG.secret_key
