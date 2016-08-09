from functools import wraps

from flask import flash, redirect, url_for, session
from .model import db, User

admins = ["admin@phoenixnow.com","23alic@gmail.com"]

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if "email" in session:
            return func(*args, **kwargs)
        else:
            flash("Error accessing page - not logged in")
            return redirect(url_for("regular.signin"))
    return wrap

def login_notrequired(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if "email" not in session:
            return func(*args, **kwargs)
        else:
            flash("Error accessing page - already logged in")
            return redirect(url_for("regular.profile"))
    return wrap

def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session['email'] in admins:
            return func(*args, **kwargs)
        else:
            flash("Error accessing page - admin priviledges needed")
            return redirect(url_for("regular.profile"))
    return wrap

def check_verified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(email = session['email']).first()
        if user.verified is False:
            flash('Please verify your account!', 'warning')
            return redirect(url_for('regular.unverified'))
        return func(*args, **kwargs)

    return decorated_function

def check_notverified(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(email = session['email']).first()
        if user.verified is True:
            flash("You are already verified")
            return redirect(url_for('regular.profile'))
        return func(*args, **kwargs)

    return decorated_function
