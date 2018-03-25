"""Widoki aplikacji"""

from main import APP
from main import DB
from main import BCRYPT
from main import LM
from flask import render_template, redirect, request, session, flash
from passlib.hash import sha256_crypt
from models import User
from functools import wraps
import gc
from flask_login import login_user, logout_user, current_user

__author__ = 'Patryk Niedźwiedziński'

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            return redirect('/login/')
        else:
            return func(*args, **kwargs)
    return wrap

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

@APP.route('/register/', methods=["GET", "POST"])
def register():
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
            return redirect('/login/')
        return redirect('/login/')
    except Exception as error:
        flash('Błąd: '+str(error), 'danger')
        return redirect('/')


@APP.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('Już jesteś zalogowany!', 'warning')
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
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
@login_required
def admin():
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except Exception:
        admin = False
    if admin:
        return render_template('admin.html', admin=admin)
    return redirect('/')


@APP.route('/delete/<int:id>/')
@login_required
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
@login_required
def user_list():
    """wyświetla listę użytkowników wraz z linkami dla adminów do edycji kont użytkowników"""
    """nie wyświetla użytkownika piotr"""
    try:
        admin = User.query.filter_by(username=current_user.username).first().admin
    except KeyError:
        admin = False
    if User.query.filter_by(username=current_user.username).first().admin:
        users=User.query.order_by(User.id.asc()).all()
        admini = 0
        for user in users:
            if user.admin:
                admini += 1
        return render_template('user_list.html', users=users, admini=admini, admin=admin)
    flash('Nie możesz tego zrobić!', 'warning')
    return redirect('/')

@APP.route('/admin/ban/<username>')
@login_required
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
@login_required
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
@login_required
def give_admin(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(
                id=id).first() and User.query.filter_by(id=id).first() != User.query.filter_by(
                username=current_user.username).first():
            try:
                User.query.filter_by(id=id).first().admin = True
                User.query.filter_by(id=id).first().a = True
                DB.session.commit()
                flash('Przekazano uprawnienia administratora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except:
                return redirect('/')
    return redirect('/')

@APP.route('/take-admin/<int:id>')
@login_required
def take_admin(id):
    if id != 1:
        if User.query.filter_by(username=current_user.username).first().admin and User.query.filter_by(id=id).first():
            try:
                User.query.filter_by(id=id).first().admin = False
                User.query.filter_by(id=id).first().a = False
                DB.session.commit()
                flash('Odebrano uprawnienia administratora użytkownikowi ' + str(
                    User.query.filter_by(id=id).first().username), 'success')
                return redirect('/admin/user-list')
            except:
                return redirect('/')
    return redirect('/')


APP.secret_key = "sekretny klucz"
