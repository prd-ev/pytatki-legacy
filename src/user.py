"""Obsluga uzytkownika"""

__author__ = "Patryk Niedzwiedzinski"

from main import APP
from src.views import login_manager
from src.models import User
from flask import render_template, redirect, flash
from flask_login import current_user


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



