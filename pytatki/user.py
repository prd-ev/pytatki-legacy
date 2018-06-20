# -*- coding: utf-8 -*-
"""Obsluga uzytkownika"""

__author__ = "Patryk Niedzwiedzinski"

from main import APP, MAIL
from pytatki.database import DB
from config import CONFIG
from pytatki.models import User
from flask import render_template, redirect, flash, request, abort
from flask_login import current_user
from passlib.hash import hex_sha1
from flask_mail import Message
from passlib.hash import sha256_crypt
from pytatki.view_manager import login_manager
from itsdangerous import URLSafeTimedSerializer


ts = URLSafeTimedSerializer(CONFIG.secret_key)


@APP.route('/user/<username>/')
@login_manager
def user_info(username):
    user=User.query.filter_by(username=username).first()
    if user:
        return render_template('user.html', user=user)
    flash('Nie ma takiego użytkownika', 'warning')
    return redirect('/')


def send_confirmation_email(user = current_user):
    print(user.email)
    token = ts.dumps(user.email, salt='email-confirm-key')
    msg = Message("Pytatki - Potwierdź swój adres email", sender=CONFIG.EMAIL, recipients=[user.email])
    msg.html = "Potwierdź adres email: <a href='" + str(request.host_url) + "user/confirm/" + token + "'>link</a>"
    MAIL.send(msg)


@APP.route('/user/send-confirmation-mail/')
def send_confirmation_view():
    send_confirmation_email()
    flash("Wysłano ponownie wiadomość!", 'success')
    return redirect("/")


@APP.route('/user/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404) 
    user = User.query.filter_by(email=email).first_or_404() 
    user.confirm_mail = True
    DB.session.add(user)
    DB.session.commit()
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
