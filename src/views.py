"""Widoki aplikacji"""
import os
import re
import gc
from datetime import datetime
from sqlalchemy import func, and_
from flask import render_template, redirect, request, session, flash, url_for, send_file
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from flask_login import login_user, logout_user, current_user
from main import APP, DB
from config import CONFIG
from src.models import User, Subject, Topic, Note
from src.user import send_confirmation_email
from src.view_manager import ban, login_required, login_manager, nocache


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

def valid_password(password):
    """Validation of password"""
    return re.search('[0-9]', password) and re.search('[A-Z]', password) \
        and re.search('[a-z]', password)

def valid_username(username):
    """Validation of username"""
    return " " in username and username == username.lower()

@APP.route('/register/', methods=["POST"])
def register_post():
    """Function for registration a new user"""
    #try:
    if not current_user.is_authenticated:
        form = request.form
        try:
            if form['password'] == form['confirm'] and len(
                    form['password']) >= 8 and valid_password(form['password']):
                password = sha256_crypt.encrypt((str(form['password'])))
                wrong_password = False
            else:
                wrong_password = True
        except KeyError:
            wrong_password = True
        try:
            accept = form['accept_tos']
        except KeyError:
            accept = ''
        used_username = User.query.filter_by(username=form['username']).first()
        if accept != 'checked' or used_username or '@' not in form['email'] \
            or wrong_password or valid_username(form['username']):
            return render_template(
                'register.html',
                form=form,
                not_accept=bool(accept != 'checked'),
                used_username=used_username,
                wrong_email=bool('@' not in form['email']),
                wrong_password=wrong_password,
                wrong_username=bool(' ' in form['username']),
                upper=bool(not form['username'] == form['username'].lower()),
                )
        user = User(username=form['username'], password=password,
                    email=form['email'])
        DB.session.add(user)
        DB.session.commit()
        flash("Zarejestrowano pomyslnie!", 'success')
        send_confirmation_email(user)
        return redirect(url_for('login', next=request.args.get('next'), username=form['username']))
    else:
        flash("Jestes juz zalogowany!", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')
    #except Exception as error:
    #    flash('Blad: '+str(error), 'danger')
    #    return redirect('/')


@APP.route('/register/', methods=["GET"])
def register_get():
    """Registration a new user"""
    if not current_user.is_authenticated:
        return render_template('register.html')
    else:
        flash("Jestes juz zalogowany!", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/login/', methods=["GET", "POST"])
def login():
    """Login"""
    if current_user.is_authenticated:
        flash('Juz jestes zalogowany!', 'warning')
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect('/')
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user, remember=bool(request.form['remember']))
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        return render_template('login.html', form=request.form, wrong=True)
    else:
        return render_template('login.html')



@APP.route("/logout/")
@login_required
def logout():
    """Logout"""
    try:
        logout_user()
        return redirect('/')
    except Exception as error:
        flash('Blad: '+str(error), 'danger')
        return redirect('/')


@APP.route('/')
@ban
def homepage():
    """Homepage"""
    if current_user.is_authenticated:
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        topics = Topic.query.order_by(Topic.id.asc()).all()
        notes = Note.query.order_by(Note.id.asc()).all()
        return render_template('homepage.html', subjects=subjects,
                               topics=topics, notes=notes)
    return render_template('homepage.html')


@APP.route('/about/')
def about():
    """About"""
    return render_template('about.html')


@APP.route("/admin/")
@login_manager
def admin():
    """Admin"""
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except Exception:
        admin = False
    if admin or User.query.filter_by(username=current_user.username).first().modderator:
        return render_template('admin.html', admin=admin)
    flash("Nie mozesz tego zrobic", 'warning')
    return redirect('/')


@APP.route('/admin/delete/user/<int:identifier>/', methods=["GET"])
@login_manager
def delete_user(identifier):
    """Delete user"""
    if not User.query.filter_by(id=identifier).first().superuser:
        if identifier == User.query.filter_by(username=current_user.username).first().id \
        or User.query.filter_by(username=current_user.username).first().admin:
            user = User.query.filter_by(id=identifier).first()
            if user:
                if identifier == User.query.filter_by(username=current_user.username).first().id:
                    try:
                        logout_user()
                        DB.session.delete(user)
                        DB.session.commit()
                        gc.collect()
                        session.clear()
                        gc.collect()
                        flash('Twoje konto zostalo usuniete', 'success')
                    except Exception as error:
                        flash('Blad: '+str(error), 'danger')
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
    if current_user.admin or current_user.modderator:
        note = Note.query.filter_by(id=identifier).first()
        if note:
            try:
                os.remove(os.path.join(APP.config['UPLOAD_FOLDER'], note.file))
                DB.session.delete(note)
                DB.session.commit()
                flash('Notatka zostala usunieta!', 'success')
            except Exception as error:
                flash('Blad: '+str(error), 'danger')
        else:
            flash('Nie ma takiej notatki', 'warning')
    else:
        flash('Nie mozesz tego zrobic!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/subject/<int:identifier>/', methods=["GET"])
@login_manager
def delete_subject(identifier):
    """Delete subject"""
    if current_user.admin or current_user.modderator:
        subject = Subject.query.filter_by(id=identifier).first()
        if subject:
            try:
                DB.session.delete(subject)
                for topic in Topic.query.order_by(Topic.id.asc()).all():
                    if topic.subject_id == identifier:
                        DB.session.delete(topic)
                for note in Note.query.order_by(Note.id.asc()).all():
                    if note.subject_id == identifier:
                        DB.session.delete(note)
                DB.session.commit()
                flash('Przedmiot zostal usuniety!', 'success')
            except Exception as error:
                flash('Blad: '+str(error), 'danger')
        else:
            flash('Nie ma takiego przedmiotu', 'warning')
    else:
        flash('Nie mozesz tego zrobic!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/topic/<int:identifier>/', methods=["GET"])
@login_manager
def delete_topic(identifier):
    """Delete topic"""
    if current_user.admin or current_user.modderator:
        topic = Topic.query.filter_by(id=identifier).first()
        if topic:
            try:
                DB.session.delete(topic)
                for note in Note.query.order_by(Note.id.asc()).all():
                    if note.topic_id == identifier:
                        DB.session.delete(note)
                DB.session.commit()
                flash('Dzial zostal usuniety!', 'success')
            except Exception as error:
                flash('Blad: '+str(error), 'danger')
        else:
            flash('Nie ma takiego dzialu', 'warning')
    else:
        flash('Nie mozesz tego zrobic!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route("/admin/user-list/")
@login_manager
def user_list():
    """wyswietla liste uzytkownikow"""
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except KeyError:
        admin = False
    if User.query.filter_by(username=current_user.username).first().admin \
    or User.query.filter_by(username=current_user.username).first().modderator:
        users = User.query.order_by(User.id.asc()).all()
        admini = 0
        for user in users:
            if user.admin:
                admini += 1
        return render_template('user_list.html', users=users, admini=admini, admin=admin)
    flash('Nie mozesz tego zrobic!', 'warning')
    return redirect('/')

@APP.route('/admin/ban/<username>/', methods=["GET"])
@login_manager
def ban_user(username):
    """Ban user"""
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = True
        DB.session.commit()
        flash('Uzytkownik '+user.username+' zostal zbanowany', 'success')
    else:
        flash('Nie ma takiego uzytkownika', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/unban/<username>/', methods=["GET"])
@login_manager
def unban(username):
    """Unban user"""
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = False
        DB.session.commit()
        flash('Uzytkownik '+user.username+' zostal odbanowany', 'success')
    else:
        flash('Nie ma takiego uzytkownika', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/give-admin/<int:identifier>/', methods=["GET"])
@login_manager
def give_admin(identifier):
    """Give admin"""
    if User.query.filter_by(username=current_user.username).first().admin \
    and User.query.filter_by(id=identifier).first() \
    and User.query.filter_by(id=identifier).first() != User.query.filter_by(
            username=current_user.username).first():
        try:
            User.query.filter_by(id=identifier).first().admin = True
            DB.session.commit()
            flash('Przekazano uprawnienia administratora uzytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        except Exception as error:
            flash("Blad: "+str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/take-mod/<int:identifier>/', methods=["GET"])
@login_manager
def take_mod(identifier):
    """Take mod"""
    if User.query.filter_by(username=current_user.username).first().admin \
    and User.query.filter_by(id=identifier).first():
        try:
            User.query.filter_by(id=identifier).first().modderator = False
            DB.session.commit()
            flash('Odebrano uprawnienia moderatora uzytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        except Exception as error:
            flash("Blad: " + str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash("Nie mozna tego zrobic", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/give-mod/<int:identifier>/', methods=["GET"])
@login_manager
def give_mod(identifier):
    """Give mod"""
    if User.query.filter_by(username=current_user.username).first().admin \
    and User.query.filter_by(id=identifier).first() \
    and User.query.filter_by(id=identifier).first() != User.query.filter_by(
            username=current_user.username).first():
        try:
            User.query.filter_by(id=identifier).first().modderator = True
            DB.session.commit()
            flash('Przekazano uprawnienia moderatora uzytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
        except Exception as error:
            flash("Blad: "+str(error), 'danger')
    else:
        flash("Nie mozesz tego zrobic", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/take-admin/<int:identifier>/', methods=["GET"])
@login_manager
def take_admin(identifier):
    """take admin"""
    if not User.query.filter_by(id=identifier).first().superuser:
        if User.query.filter_by(username=current_user.username).first().admin \
        and User.query.filter_by(id=identifier).first():
            try:
                User.query.filter_by(id=identifier).first().admin = False
                DB.session.commit()
                flash('Odebrano uprawnienia administratora uzytkownikowi ' + str(
                    User.query.filter_by(id=identifier).first().username), 'success')
            except Exception as error:
                flash("Blad: " + str(error), 'danger')
        else:
            flash("Nie mozesz tego zrobic", 'warning')
    else:
        flash("Nie mozesz tego zrobic", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

def allowed_file(filename):
    """Check if file has valid name and allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                    if not os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'],
                                                       form['subject'], form['topic'])):
                        os.makedirs(os.path.join(APP.config['UPLOAD_FOLDER'], form['subject'],
                                                 form['topic']))
                        request_file.save(os.path.join(APP.config['UPLOAD_FOLDER'],
                                                       form['subject'], form['topic'], filename))
                else:
                    flash('Nieobslugiwane rozszerzenie', 'warning')
                    return redirect(request.url)
            note = Note()
            note.name = form['title']
            note.author_id = current_user.id
            note.subject_id = form['subject']
            note.topic_id = form['topic']
            note.file = os.path.join(form['subject'], form['topic'], filename)
            note.date = datetime.now()
            DB.session.add(note)
            DB.session.commit()
            flash('Notatka zostala dodana!', 'success')
            if request.args.get('next'):
                if request.args.get('next') == '/':
                    pass
                else:
                    return redirect(request.args.get('next'))
            return redirect('/#'+str(form['subject'])+'#'+str(form['topic']))
        except Exception as error:
            flash("Blad: " + str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    else:
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        topics = Topic.query.order_by(Topic.id.asc()).all()
        return render_template('add.html', subjects=subjects, topics=topics)

@APP.route('/admin/add/', methods=["POST"])
@login_manager
def admin_add_post():
    """Admin add"""
    if current_user.admin or current_user.modderator:
        if request.form['type'] == 'subject':
            try:
                if Subject.query.filter(func.lower(Subject.name) == func.lower(
                        request.form['title'])).first():
                    flash("Dany przedmiot juz istnieje", 'warning')
                else:
                    subject = Subject()
                    subject.name = request.form['title']
                    DB.session.add(subject)
                    DB.session.commit()
                    flash('Dodano przedmiot!', 'success')
            except Exception as e:
                flash('Blad: '+str(e), 'danger')
        elif request.form['type'] == 'topic':
            try:
                if Topic.query.filter(and_(func.lower(Topic.name) == func.lower(
                        request.form['title']), Topic.subject_id == request.form['subject'])
                                     ).first():
                    flash("Dany dzial juz istnieje", 'warning')
                else:
                    topic = Topic()
                    topic.name = request.form['title']
                    topic.subject_id = request.form['subject']
                    DB.session.add(topic)
                    DB.session.commit()
                    flash('Dodano dzial!', 'success')
            except Exception as e:
                flash('Blad: '+str(e), 'danger')
    else:
        flash('Nie mozesz tego zrobic', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/add/', methods=["GET"])
@login_manager
def admin_add_get():
    """Admin add"""
    if current_user.admin or current_user.modderator:
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        topics = Topic.query.order_by(Topic.id.asc()).all()
        return render_template('admin_add.html', subjects=subjects, topics=topics)
    else:
        flash("Nie masz uprawnien", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/notes/')
@login_manager
def notes():
    """List of notes"""
    notes = Note.query.order_by(Note.id.asc()).all()
    return render_template('notes.html', notes=notes)

@APP.route('/admin/subjects/')
@login_manager
def subjects():
    """List of subjects"""
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    topics = Topic.query.order_by(Topic.id.asc()).all()
    return render_template('subjects.html', subjects=subjects, topics=topics)


@APP.route('/admin/subject/<identifier>/edit/', methods=['GET', 'POST'])
def edit_subject(identifier):
    """Edit subject"""
    if request.method == 'POST':
        form = request.form
        Subject.query.filter_by(id=identifier).first().name = form['name']
        DB.session.commit()
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect(request.path)
    subject = Subject.query.filter_by(id=identifier).first()
    return render_template('edit.html', subject=subject)


@APP.route('/admin/topic/<identifier>/edit/', methods=['GET', 'POST'])
def edit_topic(identifier):
    """Edit topic"""
    if request.method == 'POST':
        form = request.form
        Topic.query.filter_by(id=identifier).first().name = form['name']
        Topic.query.filter_by(id=identifier).first().subject_id = form['subject']
        DB.session.commit()
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect(request.path)
    topic = Topic.query.filter_by(id=identifier).first()
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    return render_template('edit_t.html', topic=topic, subjects=subjects)


@APP.route('/admin/note/<identifier>/edit/', methods=['GET', 'POST'])
def edit_note(identifier):
    """Edit note"""
    if request.method == 'POST':
        form = request.form
        Note.query.filter_by(id=identifier).first().name = form['name']
        Note.query.filter_by(id=identifier).first().subject_id = form['subject']
        Note.query.filter_by(id=identifier).first().topic_id = form['topic']
        if 'file' in request.files:
            if not request.files['file'].filename == '' and allowed_file(
                    request.files['file'].filename):
                filename = secure_filename(request.files['file'].filename)
                os.remove(os.path.join(APP.config['UPLOAD_FOLDER'], Note.query.filter_by(
                    id=identifier).first().file))
                request.files['file'].save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
                Note.query.filter_by(id=identifier).first().file = str(filename)
        flash('Zapisano zmiany!', 'success')
        DB.session.commit()
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect(request.path)
    note = Note.query.filter_by(id=identifier).first()
    topics = Topic.query.order_by(Topic.id.asc()).all()
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    return render_template('edit_n.html', note=note, topics=topics, subjects=subjects)


@APP.route('/download/<identifier>/')
@login_manager
@nocache
def download(identifier):
    """Download file"""
    if current_user.is_authenticated:
        note = Note.query.filter_by(id=identifier).first()
        return send_file(os.path.join(APP.config['UPLOAD_FOLDER'], note.file))
    flash("Musisz byc zalogowany", 'warning')
    return redirect('/')

APP.secret_key = CONFIG.secret_key
