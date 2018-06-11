# -*- coding: utf-8 -*-
from functools import wraps, update_wrapper
from flask_login import current_user
from flask import flash, redirect, request, url_for, make_response
from datetime import datetime

def ban(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.ban:
                flash("Twoje konto zostało zbanowane na czas nieokreślony", 'danger')
                return redirect('/logout/')
            elif not current_user.confirm_mail:
                flash('Potwierdź adres email. <a href="/user/send-confirmation-mail/">Wyślij ponownie</a>', 'warning')
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrap


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

def login_manager(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            next_url = request.path
            return redirect(url_for('login', next=next_url))
        elif current_user.is_authenticated and current_user.ban:
            flash("Twoje konto zostało zbanowane na czas nieokreślony", 'danger')
            return redirect('/logout/')
        elif not current_user.confirm_mail:
            flash('Potwierdź adres email. <a href="/user/send-confirmation-mail/">Wyślij ponownie</a>', 'warning')
            return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrap

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Musisz być zalogowany", 'warning')
            next_url = request.url
            return redirect(url_for('login', next=next_url))
        else:
            return func(*args, **kwargs)
    return wrap