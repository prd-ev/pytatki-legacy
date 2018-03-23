"""Widoki aplikacji"""

from main import APP
from main import DB
from main import BCRYPT
from main import LM
from flask import render_template, redirect, request, session
from passlib.hash import sha256_crypt
from models import User
from functools import wraps

__author__ = 'Patryk Niedźwiedziński'


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not 'logged_in' in session:
            return redirect('/')
        else:
            return func(*args, **kwargs)
    return wrap


user = User()


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
            if "@" not in email:
                wrong_email=True
            else:
                wrong_email=False
            if not_accept or used_username or wrong_email or wrong_password:
                return render_template('register.html', form=form, not_accept=not_accept, used_username=used_username,
                                       wrong_email=wrong_email, wrong_password=wrong_password)
            user.email = email
            user.password = password
            user.username = username
            DB.session.add(user)
            DB.session.commit()
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
    except Exception as error:
        print(error)
        return redirect('/')


@APP.route('/login/', methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            db_user = User.query.filter_by(username=request.form['username']).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(request.form['password'], db_password):
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    db_user.active = 1
                    DB.session.commit()
                    return redirect('/')
            db_user = User.query.filter_by(email=request.form['username']).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(request.form['password'], db_password):
                    session['logged_in'] = True
                    session['username'] = User.query.filter_by(email=request.form['username']).first().username
                    session['email'] = User.query.filter_by(email=request.form['username']).first().email
                    db_user.active = 1
                    DB.session.commit()
                    return redirect('/')
            else:
                return render_template('login.html', form=request.form, wrong=True)
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')


@APP.route("/logout/")
@login_required
def logout():
    """Wylogowuje ustawiając status na niaktywny"""
    try:
        User.query.filter_by(username=session['username']).first().active = 0
        DB.session.commit()
        session.clear()
        return redirect('/')
    except Exception as e:
        return redirect('/')


@APP.route('/')
def homepage():
    try:
        admin = User.query.filter_by(username=session['username']).first().admin
    except KeyError:
        admin = False
    return render_template('homepage.html', admin=admin)


APP.secret_key = "sekretny klucz"
