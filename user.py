"""Obsluga uzytkownika"""

__author__ = "Patryk Niedzwiedzinski"

from main import APP
from views import ban, login_manager
from models import User, Note, Subject, Topic
from flask import request, render_template, redirect, flash
from flask_login import current_user
from flask_mail import Message


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



