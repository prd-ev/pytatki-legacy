"""Widoki aplikacji"""

from main import APP
from main import DB
from main import BCRYPT
from main import LM
from config import CONFIG
from flask import render_template, redirect, request, session, flash, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from models import User, Subject, Topic, Note
from functools import wraps, update_wrapper
import gc
from flask_login import login_user, logout_user, current_user
from datetime import datetime
import os

__author__ = 'Patryk Niedźwiedziński'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ban(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.ban:
                flash("Twoje konto zostało zbanowane na czas nieokreślony", 'danger')
                return redirect('/logout/')
            else:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrap


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

def login_manager(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            next_url = request.path
            return redirect(url_for('login', next=next_url))
        else:
            if current_user.is_authenticated:
                if current_user.ban:
                    flash("Twoje konto zostało zbanowane na czas nieokreślony", 'danger')
                    return redirect('/logout/')
                else:
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
    return wrap

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            next_url = request.url
            return redirect(url_for('login', next=next_url))
        else:
            return func(*args, **kwargs)
    return wrap

@APP.route('/register/', methods=["GET", "POST"])
def register():
    next_url = request.args.get('next')
    if not current_user.is_authenticated:
        try:
            if request.method == "POST":
                form = request.form
                username = form['username']
                if username == username.lower():
                    upper = False
                else:
                    upper = True
                email = form['email']
                try:
                    if form['password']==form['confirm'] and not form['password']=='':
                        password = sha256_crypt.encrypt((str(form['password'])))
                        wrong_password=False
                    else:
                        wrong_password = True
                except Exception:
                    wrong_password = True
                try:
                    accept = form['accept_tos']
                    if not accept == 'checked':
                        not_accept=True
                    else:
                        not_accept=False
                except Exception:
                    not_accept=True
                used_username = User.query.filter_by(username=username).first()
                if used_username:
                    used_username=True
                else:
                    used_username=False
                if " " in username:
                    wrong_username = True
                else:
                    wrong_username = False
                if "@" not in email:
                    wrong_email=True
                else:
                    wrong_email=False
                if not_accept or used_username or wrong_email or wrong_password or wrong_username or upper:
                    return render_template('register.html', form=form, not_accept=not_accept,
                                           used_username=used_username, wrong_email=wrong_email,
                                           wrong_password=wrong_password, wrong_username=wrong_username, upper=upper)
                user = User(username=username, password=password, email=email)
                DB.session.add(user)
                DB.session.commit()
                flash("Zarejestrowano pomyślnie!", 'success')
                return redirect(url_for('login', next=next_url, username=username))
            else:
                return render_template('register.html')
        except Exception as error:
            flash('Błąd: '+str(error), 'danger')
            return redirect('/')
    else:
        flash("Jesteś już zalogowany!", 'warning')
        return redirect(next_url)


@APP.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('Już jesteś zalogowany!', 'warning')
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect('/')
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        return render_template('login.html', form=request.form, wrong=True)
    else:
        return render_template('login.html')



@APP.route("/logout/")
@login_required
def logout():
    try:
        logout_user()
        return redirect('/')
    except Exception as e:
        flash('Błąd: '+str(e), 'danger')
        return redirect('/')


@APP.route('/')
@ban
def homepage():
    if current_user.is_authenticated:
        try:
            admin = User.query.filter_by(username=current_user.username).first().admin
        except Exception:
            admin = False
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        topics = Topic.query.order_by(Topic.id.asc()).all()
        notes = Note.query.order_by(Note.id.asc()).all()
        return render_template('homepage.html', admin=admin, subjects=subjects, topics=topics, notes=notes)
    else:
        admin = False
    return render_template('homepage.html', admin=admin)


@APP.route('/about/')
def about():
    return render_template('about.html')


@APP.route('/user/<username>/')
@ban
def user_info(username):
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except Exception:
        admin = False
    user=User.query.filter_by(username=username).first()
    if user:
        return render_template('user.html', user=user, admin=admin)
    else:
        flash('Nie ma takiego użytkownika', 'warning')
        return redirect('/')


@APP.route("/admin/")
@login_manager
def admin():
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except Exception:
        admin = False
    if admin or User.query.filter_by(username=current_user.username).first().modderator:
        return render_template('admin.html', admin=admin)
    flash("Nie możesz tego zrobić", 'warning')
    return redirect('/')


@APP.route('/admin/delete/user/<int:identifier>/', methods=["GET"])
@login_manager
def delete_user(identifier):
    if not User.query.filter_by(id=identifier).first().superuser:
        if identifier == User.query.filter_by(username=current_user.username).first().id or User.query.filter_by(
                username=current_user.username).first().admin:
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
                        flash('Twoje konto zostało usunięte', 'success')
                        return redirect('/')
                    except Exception as e:
                        flash('Błąd: '+str(e), 'danger')
                        return redirect('/')
                else:
                    DB.session.delete(user)
                    DB.session.commit()
                    flash('Użytkownik został usunięty', 'success')
                    if request.args.get('next'):
                        return redirect(request.args.get('next'))
                    return redirect('/')
            else:
                flash('Nie ma takiego użytkownika', 'warning')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
    flash('Nie możesz tego zrobić!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/note/<int:identifier>/', methods=["GET"])
@login_manager
def delete_note(identifier):
    if current_user.admin or current_user.modderator:
        note = Note.query.filter_by(id=identifier).first()
        if note:
            try:
                DB.session.delete(note)
                DB.session.commit()
                flash('Notatka została usunięta!', 'success')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
            except Exception as e:
                flash('Błąd: '+str(e), 'danger')
                return redirect('/')

        else:
            flash('Nie ma takiej notatki', 'warning')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash('Nie możesz tego zrobić!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/subject/<int:identifier>/', methods=["GET"])
@login_manager
def delete_subject(identifier):
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
                flash('Przedmiot został usunięty!', 'success')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
            except Exception as e:
                flash('Błąd: '+str(e), 'danger')
                return redirect('/')

        else:
            flash('Nie ma takiego przedmiotu', 'warning')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash('Nie możesz tego zrobić!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/delete/topic/<int:identifier>/', methods=["GET"])
@login_manager
def delete_topic(identifier):
    if current_user.admin or current_user.modderator:
        topic = Topic.query.filter_by(id=identifier).first()
        if topic:
            try:
                DB.session.delete(topic)
                for note in Note.query.order_by(Note.id.asc()).all():
                    if note.topic_id == identifier:
                        DB.session.delete(note)
                DB.session.commit()
                flash('Dział został usunięty!', 'success')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
            except Exception as e:
                flash('Błąd: '+str(e), 'danger')
                return redirect('/')

        else:
            flash('Nie ma takiego działu', 'warning')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash('Nie możesz tego zrobić!', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route("/admin/user-list/")
@login_manager
def user_list():
    """wyświetla listę użytkowników wraz z linkami dla adminów do edycji kont użytkowników"""
    """nie wyświetla użytkownika piotr"""
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except KeyError:
        admin = False
    if User.query.filter_by(username=current_user.username).first().admin or User.query.filter_by(username=current_user.username).first().modderator:
        users=User.query.order_by(User.id.asc()).all()
        admini = 0
        for user in users:
            if user.admin:
                admini += 1
        return render_template('user_list.html', users=users, admini=admini, admin=admin)
    flash('Nie możesz tego zrobić!', 'warning')
    return redirect('/')

@APP.route('/admin/ban/<username>/', methods=["GET"])
@login_manager
def ban(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = True
        DB.session.commit()
        flash('Użytkownik '+user.username+' został zbanowany', 'success')
    else:
        flash('Nie ma takiego użytkownika', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/unban/<username>/', methods=["GET"])
@login_manager
def unban(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = False
        DB.session.commit()
        flash('Użytkownik '+user.username+' został odbanowany', 'success')
    else:
        flash('Nie ma takiego użytkownika', 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/give-admin/<int:identifier>/', methods=["GET"])
@login_manager
def give_admin(identifier):
    if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(
            id=identifier).first() and User.query.filter_by(id=identifier).first() != User.query.filter_by(
            username=current_user.username).first():
        try:
            User.query.filter_by(id=identifier).first().admin = True
            DB.session.commit()
            flash('Przekazano uprawnienia administratora użytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        except Exception as error:
            flash("Błąd: "+str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/take-mod/<int:identifier>/', methods=["GET"])
@login_manager
def take_mod(identifier):
    if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(id=identifier).first():
        try:
            User.query.filter_by(id=identifier).first().modderator = False
            DB.session.commit()
            flash('Odebrano uprawnienia moderatora użytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        except Exception as error:
            flash("Błąd: "+str(error),'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash("Nie można tego zrobić", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/give-mod/<int:identifier>/', methods=["GET"])
@login_manager
def give_mod(identifier):
    if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(
            id=identifier).first() and User.query.filter_by(id=identifier).first() != User.query.filter_by(
            username=current_user.username).first():
        try:
            User.query.filter_by(id=identifier).first().modderator = True
            DB.session.commit()
            flash('Przekazano uprawnienia moderatora użytkownikowi ' + str(
                User.query.filter_by(id=identifier).first().username), 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
        except Exception as error:
            flash("Błąd: "+str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    flash("Nie możesz tego zrobić", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

@APP.route('/admin/take-admin/<int:identifier>/', methods=["GET"])
@login_manager
def take_admin(identifier):
    if not User.query.filter_by(id=identifier).first().superuser:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(id=identifier).first():
            try:
                User.query.filter_by(id=identifier).first().admin = False
                DB.session.commit()
                flash('Odebrano uprawnienia administratora użytkownikowi ' + str(
                    User.query.filter_by(id=identifier).first().username), 'success')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
            except:
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
    flash("Nie możesz tego zrobić", 'warning')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP.route('/add/', methods=["GET", "POST"])
@login_manager
def add():
    if request.method == 'POST':
        try:
            form = request.form
            if 'file' not in request.files:
                flash('Błąd: No file part', 'danger')
                return redirect(request.url)
            request_file = request.files['file']
            if request_file.filename == '':
                flash('Nie wybrano pliku', 'warning')
                return redirect(request.url)
            if request_file and allowed_file(request_file.filename):
                filename = secure_filename(request_file.filename)
                request_file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
            note = Note()
            note.name = form['title']
            note.author_id = current_user.id
            note.subject_id = form['subject']
            note.topic_id = form['topic']
            note.file = str(filename)
            note.date = datetime.now()
            DB.session.add(note)
            DB.session.commit()
            flash('Notatka została dodana!', 'success')
            if request.args.get('next'):
                if request.args.get('next')=='/':
                    pass
                else:
                    return redirect(request.args.get('next'))
            return redirect('/#'+str(form['subject'])+'#'+str(form['topic']))
        except Exception as error:
            flash("Błąd: " + str(error), 'danger')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            return redirect('/')
    else:
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        topics = Topic.query.order_by(Topic.id.asc()).all()
        return render_template('add.html', subjects=subjects, topics=topics)

@APP.route('/admin/add/', methods=["GET", "POST"])
@login_manager
def admin_add():
    if current_user.admin or current_user.modderator:
        if request.method == 'POST':
            if request.form['type']=='subject':
                try:
                    subject = Subject()
                    subject.name = request.form['title']
                    DB.session.add(subject)
                    DB.session.commit()
                    flash('Dodano przedmiot!', 'success')
                except Exception as e:
                    flash('Błąd: '+str(e), 'danger')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
            elif request.form['type'] == 'topic':
                try:
                    topic = Topic()
                    topic.name = request.form['title']
                    topic.subject_id = request.form['subject']
                    DB.session.add(topic)
                    DB.session.commit()
                    flash('Dodano dział!', 'success')
                except Exception as e:
                    flash('Błąd: '+str(e), 'danger')
                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                return redirect('/')
        else:
            subjects = Subject.query.order_by(Subject.id.asc()).all()
            topics = Topic.query.order_by(Topic.id.asc()).all()
            return render_template('admin_add.html', subjects=subjects, topics=topics)
    else:
        flash('Nie możesz tego zrobić', 'warning')
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect('/')

@APP.route('/admin/notes/')
@login_manager
def notes():
    notes = Note.query.order_by(Note.id.asc()).all()
    return render_template('notes.html', notes=notes)

@APP.route('/admin/subjects/')
@login_manager
def subjects():
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    topics = Topic.query.order_by(Topic.id.asc()).all()
    return render_template('subjects.html', subjects=subjects, topics=topics)

@APP.route('/download/<filename>/')
@login_manager
@nocache
def download(filename):
    if current_user.is_authenticated:
        return send_from_directory(APP.config['UPLOAD_FOLDER'], filename)
    else:
        flash("Musisz być zalogowany", 'warning')
        return redirect('/')

APP.secret_key = CONFIG.secret_key
