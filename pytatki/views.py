"""Widoki aplikacji"""
import json
import os

from flask import (flash, g, jsonify, redirect, render_template, request,
                   send_file)
from flask_login import current_user
from pymysql import escape_string
from werkzeug.utils import secure_filename

from pytatki import __version__
from pytatki.dbconnect import (connection, create_note, has_access_to_note,
                               has_access_to_notegroup,
                               note_exists, notegroup_empty, remove_note,
                               remove_notegroup, add_user_to_usergroup)
from pytatki.main import APP, CONFIG
from pytatki.models import get_user
from pytatki.view_manager import login_manager, nocache
from pytatki.security import ts

__author__ = 'Patryk Niedzwiedzinski'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'xslx', 'xsl', 'odt',
                      'rtf', 'cpp'}


def find_notegroup_children(id_notegroup, id_user):
    """Generate dict with recurent children of usergroup"""
    if id_notegroup == 0 or not int(id_notegroup) or id_user == 0 or not int(id_user):
        return "ID must be a valid positive integer"
    children = []
    if has_access_to_notegroup(id_notegroup, id_user):
        con, conn = connection()
        con.execute("SELECT idnotegroup, folder_name FROM notegroup_view WHERE iduser = %s AND parent_id = %s", (
            escape_string(str(id_user)), escape_string(str(id_notegroup))))
        usergroups = con.fetchall()
        con.execute(
            "SELECT idnote, value, note_type, creator_login, notegroup_id, notegroup_name, title AS 'name' FROM "
            "note_view WHERE notegroup_id = %s AND status_id = 1",
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


def add_tag_to_note(tag, id_note, id_user):
    """Add tag to note, if tag doesn't exist create new"""
    if has_access_to_note(id_note, id_user):
        con, conn = connection()
        con.execute("SELECT * FROM tag WHERE name = %s", escape_string(tag))
        tag = con.fetchone()
        if not tag:
            conn.begin()
            con.execute("INSERT INTO tag (name) VALUES (%s)",
                        escape_string(tag))
            tag_id = con.lastrowid
            conn.commit()
        else:
            tag_id = tag['idtag']
        conn.begin()
        con.execute("INSERT INTO tagging (note_id, tag_id) VALUES (%s, %s)",
                    (escape_string(str(id_note)), escape_string(str(tag_id))))
        conn.commit()
        con.execute("SELECT * FROM note_tags WHERE idnote = %s",
                    escape_string(str(id_note)))
        note = con.fetchone()
        con.close()
        conn.close()
        return note


def post_note(title="xxd", type_name="text", value="xd", id_notegroup=1, id_user=1):
    """Post a note to database"""
    if not has_access_to_notegroup(id_notegroup, id_user):
        return "Access denied"
    if type_name == "file":
        return "File type is not supported via GraphQL"
    con, conn = connection()
    con.execute("SELECT idnote FROM note WHERE title = %s AND notegroup_id = %s", (
        escape_string(title), escape_string(str(id_notegroup))))
    used_name = con.fetchone()
    if used_name:
        con.close()
        conn.close()
        return "Cannot add note: used title"
    conn.begin()
    con.execute("INSERT INTO note (value, title, note_type_id, user_id, notegroup_id) VALUES (%s, %s, %s, %s, %s)", (
        escape_string(value), escape_string(title), escape_string(
            str(type_id(type_name))), escape_string(str(id_user)),
        escape_string(str(id_notegroup))))
    note_id = con.lastrowid
    con.execute("INSERT INTO action (content, user_id, note_id) VALUES (\"Create\", %s, %s)", (
        escape_string(str(id_user)), escape_string(str(note_id))))
    conn.commit()
    con.execute("SELECT * FROM note_view WHERE idnote = %s",
                escape_string(str(note_id)))
    note = con.fetchone()
    return note


@APP.route('/')
def homepage():
    if current_user.is_authenticated:
        return redirect('/app/')
    return render_template('landing_page.html')


@APP.route('/app/')
def app_view():
    return render_template('react.html')


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
    # TODO: delete user
    return jsonify({'data': "This function is not avaliable in this version: \'{}\'".format(str(__version__))})


@APP.route('/notegroup/<int:identifier>/delete/', methods=['GET'])
def delete_notegroup(identifier):
    con, conn = connection()
    if notegroup_empty(identifier):
        conn.begin()
        remove_notegroup(conn, identifier)
        conn.commit()
        con.close()
        conn.close()
        return jsonify({'data': 'success'})
    con.close()
    conn.close()
    return jsonify({'data': 'notegroup not empty'})


@APP.route('/admin/delete/note/<int:identifier>/', methods=["GET"])
@login_manager
def delete_note(identifier):
    """Delete note"""
    if current_user.is_admin:
        con, conn = connection()
        if note_exists(idnote=identifier):
            conn.begin()
            remove_note(conn, identifier, current_user['iduser'])
            conn.commit()
            con.close()
            conn.close()
            return jsonify({'data': 'Notatka zostala usunieta!'})
        con.close()
        conn.close()
        return jsonify({'data': 'Nie ma takiej notatki'})
    return jsonify({'data': 'Nie mozesz tego zrobic!'})


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
        users = []
        for user_dict in users_raw:
            user = get_user(id_user=user_dict['iduser'])
            users.append(user)
        return render_template('user_list.html', users=users)
    flash('Nie mozesz tego zrobic!', 'warning')
    return redirect('/')


@APP.route('/admin/give-admin/<int:identifier>/', methods=["GET"])
@login_manager
def give_admin(identifier):
    """Give admin"""
    con, conn = connection()
    con.execute("SELECT * FROM user WHERE iduser = %s",
                escape_string(identifier))
    user = con.fetchone()
    if current_user.is_admin and user and user['iduser'] != current_user:
        try:
            con.execute("INSERT INTO user_membership (user_id, usergroup_id) VALUES (%s, %s)",
                        (escape_string(user['iduser']), CONFIG['IDENTIFIERS']['admingroup_id']))
            conn.commit()
            flash('Przekazano uprawnienia administratora uzytkownikowi ' + str(
                user['login']), 'success')
        except Exception as error:
            flash("Error: " + str(error), 'danger')
    return redirect(request.args.get('next') if 'next' in request.args else '/')


@APP.route('/admin/take-admin/<int:identifier>/', methods=["GET"])
@login_manager
def take_admin(identifier):
    """take admin"""
    if int(identifier) != int(CONFIG['IDENTIFIERS']['admin_id']):
        con, conn = connection()
        query = con.execute(
            "SELECT iduser, login FROM user WHERE iduser = %s", escape_string(identifier))
        user = con.fetchone()
        if current_user.is_admin and query:
            try:
                con.execute("DELETE FROM user_membership WHERE user_id = %s AND usergroup_id = %s",
                            (escape_string(identifier), escape_string(int(CONFIG['IDENTIFIERS']['admingroup_id']))))
                conn.commit()
                flash('Odebrano uprawnienia administratora uzytkownikowi ' +
                      user['login'], 'success')
            except Exception as error:
                flash("Error: " + str(error), 'danger')
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
    """Add new file"""
    if request.method == 'POST':
        if note_exists(title=request.form['title'], notegroup_id=request.form['notegroup_id']):
            return jsonify({'data': 'name in use'}), 400
        form = request.form
        if 'file' not in request.files:
            return jsonify({'data': 'No file part'})
        request_file = request.files['file']
        if request_file.filename == '':
            return jsonify({'data': 'Nie wybrano pliku'})
        if request_file:
            if allowed_file(request_file.filename):
                filename = secure_filename(request_file.filename)
            else:
                return jsonify({'data': "File unsecure"})
            if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['notegroup_id'], filename)):
                if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['notegroup_id'])):
                    os.makedirs(os.path.join(
                        APP.config['UPLOAD_FOLDER'], form['notegroup_id']))
                request_file.save(os.path.join(
                    APP.config['UPLOAD_FOLDER'], form['notegroup_id'], filename))
        else:
            return jsonify({'data': 'Nieobslugiwane rozszerzenie'}), 501
        con, conn = connection()
        conn.begin()
        added = create_note(
            conn,
            str(os.path.join(form['notegroup_id'], filename)),
            form['title'],
            CONFIG['IDENTIFIERS']['note_type_file_id'],
            current_user['iduser'],
            form['notegroup_id'],
            CONFIG['IDENTIFIERS']['status_active_id'])
        conn.commit()
        con.close()
        conn.close()
        if not added:
            return jsonify({'data': 'failed'}), 500
        return jsonify({'data': 'Notatka zostala dodana!'}), 201
    else:
        con, conn = connection()
        con.execute(
            "SELECT * FROM notegroup_view WHERE iduser = %s",
            escape_string(str(current_user['iduser'])))
        topics = con.fetchall()
        con.close()
        conn.close()
        return render_template('add.html', topics=topics)


@APP.route('/admin/add/', methods=["POST"])
@login_manager
def admin_add_post():
    """Admin add"""
    if current_user.is_admin:
        con, conn = connection()
        con.execute("SELECT idnotegroup FROM notegroup_view WHERE lower(folder_name) = lower(%s) AND idusergroup = %s AND parent_id = %s",
                    (escape_string(request.form['title']),
                     escape_string(request.form['class']),
                     escape_string(request.form['parent_id']))
                    )
        if con.fetchone():
            con.close()
            conn.close()
            return jsonify({'data': "Dany przedmiot juz istnieje"})
        group = None
        if 'parent_id' in request.form:
            con.execute("SELECT idnotegroup FROM notegroup_view WHERE iduser = %s AND idnotegroup = %s",
                        (escape_string(str(current_user['iduser'])), escape_string(request.form['parent_id'])))
            group = con.fetchone()
        if group or 'parent_id' not in request.form:
            conn.begin()
            con.execute("INSERT INTO notegroup (name, parent_id) VALUES (%s, %s)", (
                escape_string(request.form['title']),
                escape_string(request.form['parent_id'] if 'parent_id' in request.form else str(0))))
            group_id = con.lastrowid
            con.execute("INSERT INTO usergroup_has_notegroup (notegroup_id, usergroup_id) VALUES (%s, %s)",
                        (escape_string(str(group_id)), escape_string(str(request.form['class']))))
            conn.commit()
            con.close()
            conn.close()
            return jsonify({'data': 'Dodano przedmiot!'})
        con.close()
        conn.close()
        return jsonify({'data': "Wystąpił błąd w zapytaniu"})
    else:
        return jsonify({'data': 'Nie mozesz tego zrobic'})
    return redirect(request.args.get('next') if 'next' in request.args else '/')


@APP.route('/admin/add/', methods=["GET"])
@login_manager
def admin_add_get():
    """Admin add"""
    if current_user.is_admin:
        con, conn = connection()
        con.execute("SELECT idnotegroup, folder_name, parent_id FROM notegroup_view WHERE iduser = %s",
                    escape_string(str(current_user['iduser'])))
        subjects = con.fetchall()
        con.execute("SELECT idusergroup, name FROM usergroup_membership WHERE iduser = %s ",
                    escape_string(str(current_user['iduser'])))
        classes = con.fetchall()
        con.close()
        conn.close()
        return render_template('admin_add.html', subjects=subjects, classes=classes)
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
            con.execute("SELECT * FROM note_view WHERE idnote = %s",
                        escape_string(identifier))
            note = con.fetchone()
            con.close()
            conn.close()
            if note['note_type'] == "file":
                return send_file(os.path.join(APP.config['UPLOAD_FOLDER'], note['value']))
            if note['note_type'] == "note":
                return redirect('/deaditor/' + identifier)
            return note['value']
    flash("Musisz byc zalogowany", 'warning')
    return redirect('/')


@APP.route('/join/<group>')
def join_group(group):
    group = ts.loads(group, salt=APP.secret_key, max_age=86400)
    con, conn = connection()
    conn.begin()
    add_user_to_usergroup(conn, current_user['iduser'], group)
    conn.commit()
    con.close()
    conn.close()
    return redirect('/app/')


@APP.route('/graphql/')
def graphql_explorer():
    return render_template("graphql.html")


@APP.route('/add_note/', methods=["GET", "POST"])
def add_note():
    """Add new note"""
    if request.method == 'POST':
        form = request.form
        if note_exists(title=form['title'], notegroup_id=form['notegroup_id']):
            return jsonify({'data': 'name in use'}), 400
        if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['notegroup_id'], form['title'], ".json")):
            if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], form['notegroup_id'])):
                os.makedirs(os.path.join(
                    APP.config['UPLOAD_FOLDER'], form['notegroup_id']))
            with open(os.path.join(
                    APP.config['UPLOAD_FOLDER'], form['notegroup_id'], form['title'] + ".json"), 'w') as note:
                note.write(
                    '{"blocks":[{"key":"7i6ti","text":"","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}')
        con, conn = connection()
        conn.begin()
        added = create_note(
            conn,
            str(os.path.join(form['notegroup_id'], form['title'] + '.json')),
            form['title'],
            CONFIG['IDENTIFIERS']['note_type_note_id'],
            current_user['iduser'],
            form['notegroup_id'],
            CONFIG['IDENTIFIERS']['status_active_id'])
        conn.commit()
        con.execute("SELECT idnote FROM note_view WHERE title = %s",
                    escape_string(form['title']))
        note = con.fetchone()
        con.close()
        conn.close()
        if not added:
            return jsonify({'data': 'failed'}), 500
        return jsonify({'data': 'Notatka numer ' + str(note['idnote']) + ' zostala dodana!'}), 201


@APP.route('/deaditor/<id>/', methods=["GET", "POST"])
def deaditor(id):
    if request.method == "POST":
        if current_user.is_authenticated:
            if has_access_to_note(id, current_user['iduser']):
                con, conn = connection()
                con.execute("SELECT * FROM note_view WHERE idnote = %s",
                            escape_string(id))
                note = con.fetchone()
                con.execute("SELECT creator_id FROM note_view WHERE idnote = %s",
                            escape_string(id))
                creator = con.fetchone()
                con.close()
                conn.close()
                if creator['creator_id']==current_user['iduser']:
                    try:
                        with open('pytatki/files/' + note['value'], 'wb') as file:
                            file.write(request.data)
                        return jsonify({"data": "Zapisanie powiodło się"})
                    except Exception as error:
                        flash(error)
                        return jsonify({"data": "Nie udało się zapisać"})
                else:
                    return jsonify({"data": "Tylko właściciel może zapisywać notatkę"})
            else:
                return jsonify({"data": "Nie masz dostępu do notatki"})
        else:
            return jsonify({"data": "Musisz być zalogowany"})


    else:
        if current_user.is_authenticated:
            if has_access_to_note(id, current_user['iduser']):
                con, conn = connection()
                con.execute("SELECT * FROM note_view WHERE idnote = %s",
                            escape_string(id))
                note = con.fetchone()
                con.execute("SELECT creator_id FROM note_view WHERE idnote = %s",
                            escape_string(id))
                creator = con.fetchone()
                con.close()
                conn.close()
                if creator['creator_id']==current_user['iduser']:
                    is_author = True
                else:
                    is_author = False
                if note['note_type'] == "note":
                    with open('pytatki/files/' + note['value'], 'r') as file:
                        data = json.load(file)
                    
                    return render_template("deaditor.html", file=data, is_author=is_author)
                return redirect("/download/" + id)
        flash("Musisz byc zalogowany", 'warning')
        return redirect('/app/')


APP.secret_key = CONFIG['DEFAULT']['secret_key']
