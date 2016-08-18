from PhoenixNow.mail import generate_confirmation_token, send_email
from flask import url_for, render_template
from PhoenixNow.model import db, User, Checkin

def create_user(first, last, grade, email, password):
    newuser = User(first, last, grade, email, password)
    db.session.add(newuser)
    db.session.commit()
    token = generate_confirmation_token(newuser.email)
    confirm_url = url_for('regular.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(newuser.email, subject, html)
    return newuser

def checkin_user(user):
    checkinObject = Checkin()
    user.checkins.append(checkinObject)
    db.session.add(checkinObject)
    user.checkedin = True
    db.session.commit()
