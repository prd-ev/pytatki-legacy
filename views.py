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
            flash("Musisz być zalogowany.")
            return redirect('/')
        else:
            return func(*args, **kwargs)
    return wrap

user=User()

@APP.route('/register/', methods=["GET", "POST"])
def register():
    """Rejestruje użytkownika dopisując go do bazy danych automatycznie logując
    i ustawiając jego status na aktywny"""
    try:
        if request.method == "POST":
            form = request.form
            username = form['username']
            email = form['email']
            password = sha256_crypt.encrypt((str(form['password'])))
            used_username = User.query.filter_by(username=username).first()
            if used_username:
                print('used')
                return render_template('register.html', form=form, used_username=True)
            if "@" not in email:
                print('wrong')
                return render_template('register.html', form=form, wrong_email=True)
            user.email = email
            user.password = password
            user.username = username
            DB.session.add(user)
            DB.session.commit()
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        return render_template('register.html', form=form)
    except Exception as error:
        return redirect('/')


@APP.route('/login/', methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            form = request.form
            db_user = User.query.filter_by(username=form['username']).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(form['password'], db_password):
                    session['logged_in'] = True
                    session['username'] = form['username']
                    db_user.active = 1
                    DB.session.commit()
                    return redirect('/')
            db_user = User.query.filter_by(email=form['username']).first()
            if db_user:
                db_password = db_user.password
                if sha256_crypt.verify(form['password'], db_password):
                    session['logged_in'] = True
                    session['username'] = User.query.filter_by(email=form['username']).first().username
                    session['email'] = User.query.filter_by(email=form['username']).first().email
                    db_user.active = 1
                    DB.session.commit()
                    return redirect('/')
            else:
                return render_template('login.html', wrong=True)
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
    return render_template('homepage.html')

APP.secret_key = "sekretny klucz"
