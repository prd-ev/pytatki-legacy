# -*- coding: utf-8 -*-
"""Obsluga uzytkownika"""

__author__ = "Patryk Niedzwiedzinski"


import re
from passlib.hash import hex_sha1, sha256_crypt
from flask_mail import Message
from flask import render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user, current_user
from main import APP, DB, MAIL
from config import CONFIG
from pytatki.models import User
from pytatki.view_manager import login_manager, login_required
from itsdangerous import URLSafeTimedSerializer


ts = URLSafeTimedSerializer(CONFIG.secret_key)


def valid_password(password):
    """Validation of password"""
    return re.search('[0-9]', password) and re.search('[A-Z]', password) \
        and re.search('[a-z]', password)


def valid_username(username):
    """Validation of username"""
    return " " in username and username == username.lower()


@APP.route('/user/<username>/')
@login_manager
def user_info(username):
    """User info"""
    user=User.query.filter_by(username=username).first()
    if user:
        return render_template('user.html', user=user)
    flash('Nie ma takiego użytkownika', 'warning')
    return redirect('/')


def send_confirmation_email(user = current_user):
    print(user.email)
    token = ts.dumps(user.email, salt='email-confirm-key')
    msg = Message("Pytatki - Potwierdź swój adres email", sender=CONFIG.EMAIL, recipients=[user.email])
    msg.html = render_template('verify_email.html', token=token)
    MAIL.send(msg)


@APP.route('/user/send-confirmation-mail/')
def send_confirmation_view():
    """Send confirmation email"""
    send_confirmation_email()
    flash("Wysłano ponownie wiadomość!", 'success')
    return redirect("/")


@APP.route('/user/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        user = User.query.filter_by(email=email).first_or_404()
        user.confirm_mail = True
        DB.session.add(user)
        DB.session.commit()
        flash("Adres email zweryfikowany!", 'success')
    except Exception as error:
        flash("Blad" + str(error), 'danger')
    return redirect('/')


@APP.route('/user/update-email/', methods=['POST'])
def update_email():
    try:
        if not current_user.email == request.form['email']:
            user = User.query.filter_by(id=current_user.id).first()
            form = request.form
            user.email = form['email']
            user.confirm_mail = False
            DB.session.commit()
            send_confirmation_email(current_user)
    except Exception as e:
        flash('Blad: ' + str(e), 'danger')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')


@APP.route('/user/update-password/', methods=['POST'])
@login_manager
def update_password():
    try:
        user = User.query.filter_by(id=current_user.id).first()
        if user.check_password(request.form['password']):
            user.password = sha256_crypt.encrypt((str(request.form['new-password'])))
            DB.session.commit()
    except Exception as e:
        flash('Blad: ' + str(e), 'danger')
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')


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


@APP.route('/login/', methods=["POST"])
def login_post():
    """Login"""
    if current_user.is_authenticated:
        flash('Juz jestes zalogowany!', 'warning')
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if not user or not user.check_password(request.form['password']):
            return render_template('login.html', form=request.form, wrong=True)
        try:
            remember = request.form['remember']
        except Exception as err:
            print(err)
            remember = False
            login_user(user, remember=remember)
    if request.args.get('next'):
        return redirect(request.args.get('next'))
    return redirect('/')


@APP.route('/login/', methods=["GET"])
def login_get():
    """Login"""
    return render_template('login.html')


@APP.route("/logout/")
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect('/')
