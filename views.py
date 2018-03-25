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

@APP.route('/register/', methods=["GET", "POST"])
def register():
    """Rejestruje użytkownika dopisując go do bazy danych automatycznie logując
    i ustawiając jego status na aktywny"""
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
                flash('Zalogowano pomyślnie!', 'success')
                return redirect('/')
        return render_template('login.html', form=request.form, wrong=True)
    else:
        return render_template('login.html')



@APP.route("/logout/")
@login_required
def logout():
    """Wylogowuje ustawiając status na niaktywny"""
    try:
        logout_user()
        flash('Zostaweł poprawnie wylogowany', 'success')
        return redirect('/')
    except Exception as e:
        flash('Błąd: '+str(e), 'danger')
        return redirect('/')


@APP.route('/')
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
def user_info(username):
    """
    Tu będą wyświetlane gamejamy, drużyny, gry i dokłade dane dotyczące użytkownika
    """
    if username==current_user.username and current_user.username=='piotr' or username!="piotr":
        try:
            admin = User.query.filter_by(username=current_user.username).first().admin
        except Exception:
            admin = False
        user=User.query.filter_by(username=username).first()
        return render_template('user.html', user=user, admin=admin)
    return redirect('/user/'+current_user.username)


@APP.route("/admin/")
@login_required
def admin():
    """to samo co user info tylko dla admina"""
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
    """NIE DZIAłA NA UŻYTKOWNIKA PIOTR"""
    """Funkcja usuwa użytkownika, po czym jeżeli zalogoway użytkownik to admin, zwraca listę użytkowników, w przeciwnym przypadku wraca na stronę główną"""
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
                return redirect('/user_list')
    flash('Nie możesz tego zrobić!', 'warning')
    return redirect('/')


APP.secret_key = "sekretny klucz"
