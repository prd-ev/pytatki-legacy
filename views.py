"""Widoki aplikacji"""

from main import APP
from main import DB
from main import BCRYPT
from main import LM
from config import CONFIG
from flask import render_template, redirect, request, session, flash, url_for
from passlib.hash import sha256_crypt
from models import User, Subject, Topic, Note
from functools import wraps
import gc
from flask_login import login_user, logout_user, current_user
from datetime import datetime
import os

__author__ = 'Patryk Niedźwiedziński'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'games')
UPLOAD_FOLDER = target
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
    next = request.args.get('next')
    if not current_user.is_authenticated:
        try:
            if request.method == "POST":
                form = request.form
                username = form['username']
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
                if not_accept or used_username or wrong_email or wrong_password or wrong_username:
                    return render_template('register.html', form=form, not_accept=not_accept, used_username=used_username,
                                           wrong_email=wrong_email, wrong_password=wrong_password, wrong_username=wrong_username)
                user = User(username=username, password=password, email=email)
                DB.session.add(user)
                DB.session.commit()
                flash("Zarejestrowano pomyślnie!", 'success')
                return redirect(url_for('login', next=next, username=username))
            else:
                return render_template('register.html')
        except Exception as error:
            flash('Błąd: '+str(error), 'danger')
            return redirect('/')
    else:
        flash("Jesteś już zalogowany!", 'warning')
        return redirect(next)


@APP.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('Już jesteś zalogowany!', 'warning')
        return redirect(request.args.get('next'))
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


@APP.route('/delete/<int:id>/')
@login_manager
def delete(id):
    if id == User.query.filter_by(username=current_user.username).first().id or User.query.filter_by(
            username=current_user.username).first().admin:
        user = User.query.filter_by(id=id).first()
        if user:
            if id == User.query.filter_by(username=current_user.username).first().id:
                logout_user()
                DB.session.delete(user)
                DB.session.commit()
                gc.collect()
                try:
                    session.clear()
                    gc.collect()
                    flash('Użytkownik został usunięty', 'success')
                    return redirect('/')
                except Exception as e:
                    flash('Błąd: '+str(e), 'danger')
                    return redirect('/')
            else:
                DB.session.delete(user)
                DB.session.commit()
                flash('Użytkownik został usunięty', 'success')
                return redirect('/admin/user-list')
        else:
            flash('Nie ma takiego użytkownika', 'warning')
            return redirect('/')
    flash('Nie możesz tego zrobić!', 'warning')
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

@APP.route('/admin/ban/<username>')
@login_manager
def ban(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = True
        DB.session.commit()
        flash('Użytkownik '+user.username+' został zbanowany', 'success')
    else:
        flash('Nie ma takiego użytkownika', 'warning')
    return redirect('/admin/user-list')

@APP.route('/admin/unban/<username>')
@login_manager
def unban(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.ban = False
        DB.session.commit()
        flash('Użytkownik '+user.username+' został odbanowany', 'success')
    else:
        flash('Nie ma takiego użytkownika', 'warning')
    return redirect('/admin/user-list')

@APP.route('/give-admin/<int:id>')
@login_manager
def give_admin(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(
                id=id).first() and User.query.filter_by(id=id).first() != User.query.filter_by(
                username=current_user.username).first():
            try:
                User.query.filter_by(id=id).first().admin = True
                DB.session.commit()
                flash('Przekazano uprawnienia administratora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except:
                return redirect('/')
    return redirect('/')

@APP.route('/take-mod/<int:id>')
@login_manager
def take_mod(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(id=id).first():
            try:
                User.query.filter_by(id=id).first().modderator = False
                DB.session.commit()
                flash('Odebrano uprawnienia moderatora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except Exception as error:
                flash("Błąd: "+str(error),'danger')
                return redirect('/')
    return redirect('/')

@APP.route('/give-mod/<int:id>')
@login_manager
def give_mod(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(
                id=id).first() and User.query.filter_by(id=id).first() != User.query.filter_by(
                username=current_user.username).first():
            try:
                User.query.filter_by(id=id).first().modderator = True
                DB.session.commit()
                flash('Przekazano uprawnienia moderatora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except:
                return redirect('/')
    return redirect('/')

@APP.route('/take-admin/<int:id>')
@login_manager
def take_admin(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(id=id).first():
            try:
                User.query.filter_by(id=id).first().admin = False
                DB.session.commit()
                flash('Odebrano uprawnienia administratora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except:
                return redirect('/')
    return redirect('/')

@APP.route('/add/', methods=["GET", "POST"])
@login_manager
def add():
    if request.method == 'POST':
        try:
            form = request.form
            note = Note()
            note.name = form['title']
            note.author_id = current_user.id
            note.subject_id = form['subject']
            note.topic_id = form['topic']
            note.date = datetime.now()
            DB.session.add(note)
            DB.session.commit()
            flash('Notatka została dodana!', 'success')
            return redirect('/')
        except Exception as error:
            flash("Błąd: " + str(error), 'danger')
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
                return redirect('/')
        else:
            subjects = Subject.query.order_by(Subject.id.asc()).all()
            topics = Topic.query.order_by(Topic.id.asc()).all()
            return render_template('admin_add.html', subjects=subjects, topics=topics)
    else:
        flash('Nie masz dostępu', 'warning')
        return redirect('/')

@APP.route('/admin/notes/')
@login_manager
def notes():
    notes = Note.query.order_by(Note.id.asc()).all()
    return render_template('notes.html', notes=notes)

@APP.route('/admin/')

@APP.route('/download/<file>/')
def download(file):
    return file


APP.secret_key = CONFIG.secret_key
