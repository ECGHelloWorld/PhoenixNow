from functools import wraps

from flask import flash, redirect, url_for, session
from .model import db, User
from flask_login import current_user

def login_notrequired(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_active:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("regular.home"))
    return wrap

def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_admin():
            return func(*args, **kwargs)
        else:
            flash("Error accessing page - admin priviledges needed")
            return redirect(url_for("regular.home"))
    return wrap

def check_verified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.verified is False:
            flash('Please verify your account!', 'warning')
            return redirect(url_for('regular.unverified'))
        return func(*args, **kwargs)

    return decorated_function

def check_notverified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.verified is True:
            flash("You are already verified")
            return redirect(url_for('regular.home'))
        return func(*args, **kwargs)

    return decorated_function
