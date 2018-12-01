# -*- coding: utf-8 -*-
"""This module contains python wrappers for managing access to endpoints."""

from pytatki import __version__ as version
from functools import wraps, update_wrapper
from flask_login import current_user
from flask import flash, redirect, request, url_for, make_response
from datetime import datetime

__author__ = u"Patryk Niedźwiedziński"
__copyright__ = "Copyright 2018, Pytatki"
__credits__ = []
__license__ = "MIT"
__version__ = version
__maintainer__ = u"Patryk Niedźwiedziński"
__email__ = "pniedzwiedzinski19@gmail.com"
__status__ = "Production"


def nocache(view) -> "view":
    """This decorator modifies response headers to set disable cache."""
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, '\
            'must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


def authentication_required(view) -> "view":
    """
    This decorator forces user to verify his email address, in order to get
    to the view.
    """
    @login_required
    @wraps(view)
    def wrap(*args, **kwargs):
        if not current_user['email_confirm']:
            flash(
                'Please confirm your email address. <a href="/user/send-confirmation-mail/">Resend</a>', 'warning')
            return view(*args, **kwargs)
        return view(*args, **kwargs)
    return wrap


def login_required(view) -> "view":
    """This decorator require user to be logged in."""
    @wraps(view)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to be logged in!", 'warning')
            next_url = request.url
            return redirect(url_for('login_get', next=next_url))
        return view(*args, **kwargs)
    return wrap


def admin_required(view):
    """This decorator require user to be an admin."""
    @login_required
    @wraps(view)
    def wrap(*args, **kwargs):
        if not current_user.is_admin:
            flash("Access denied!", 'warning')
            next_url = request.url
            return redirect(url_for('login_get', next=next_url))
        return view(*args, **kwargs)
    return wrap
