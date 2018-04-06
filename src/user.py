"""Obsluga uzytkownika"""

__author__ = "Patryk Niedzwiedzinski"

from main import APP, DB, MAIL
from config import CONFIG
from src.models import User
from flask import render_template, redirect, flash, request
from flask_login import current_user
from passlib.hash import hex_sha1
from flask_mail import Message
from src.view_manager import login_manager


@APP.route('/user/<username>/')
@login_manager
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


def send_confirmation_email(email = ''):
    if email == '':
        email = current_user.email
    token = hex_sha1.hash(email)
    msg = Message("Pytatki - Potwierdź swój adres email", sender=CONFIG.EMAIL, recipients=[email])
    msg.html = "Potwierdź adres email: <a href='" + str(request.host_url) + "user/confirm/" + token + "'>link</a>"
    MAIL.send(msg)


@APP.route('/user/send-confirmation-mail/')
def send_confirmation_view():
    send_confirmation_email()
    flash("Wysłano ponownie wiadomość!", 'success')
    return redirect("/")


@APP.route('/user/confirm/<token>')
def confirm_mail(token):
    for user in User.query.order_by(User.id.asc()).all():
        if hex_sha1.verify(user.email, token):
            user.confirm_mail = True
            DB.session.commit()
            flash('Potwierdzono adres email!', 'success')
    return redirect('/')

