"""Rejestracja"""

from main import APP, DB
from src.models import User
from src.user import send_confirmation_email
from passlib.hash import sha256_crypt
from flask import redirect, request, render_template, flash, url_for
from flask_login import current_user
import re

__author__ = 'Patryk Niedźwiedziński'


@APP.route('/register/', methods=["GET", "POST"])
def register_client():
    next_url = request.args.get('next')
    if not current_user.is_authenticated:
        try:
            if request.method == "POST":
                form = request.form
                username = form['username']
                password = None
                if username == username.lower():
                    upper = False
                else:
                    upper = True
                email = form['email']
                if form['password'] == form['confirm'] and not form['password'] == '' and len(
                        form['password']) >= 8 and re.search('[0-9]', form['password']) and re.search(
                        '[A-Z]', form['password']) and re.search('[a-z]', form['password']):
                    password = sha256_crypt.encrypt((str(form['password'])))
                    wrong_password = False
                else:
                    wrong_password = True
                accept = form['accept_tos']
                if not accept == 'checked':
                    not_accept = True
                else:
                    not_accept = False
                used_username = User.query.filter_by(username=username).first()
                if used_username:
                    used_username = True
                else:
                    used_username = False
                if " " in username:
                    wrong_username = True
                else:
                    wrong_username = False
                if "@" not in email:
                    wrong_email = True
                else:
                    wrong_email = False
                if not_accept or used_username or wrong_email or wrong_password or wrong_username or upper:
                    return render_template('register.html', form=form, not_accept=not_accept,
                                           used_username=used_username, wrong_email=wrong_email,
                                           wrong_password=wrong_password, wrong_username=wrong_username, upper=upper)
                else:
                    user = User(username=username, password=password, email=email)
                    DB.session.add(user)
                    DB.session.commit()
                    flash("Zarejestrowano pomyślnie!", 'success')
                    send_confirmation_email(email)
                return redirect(url_for('login', next=next_url, username=username))
            else:
                return render_template('register.html')
        except Exception as error:
            flash('Błąd: ' + str(error), 'danger')
            return redirect('/')
    else:
        flash("Jesteś już zalogowany!", 'warning')
        return redirect(next_url)


def register(username, password, email):
    pass
