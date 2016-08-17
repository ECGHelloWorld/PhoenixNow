from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint
from PhoenixNow.forms import SignupForm, SigninForm, ContactForm, CheckinForm
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from flask_mail import Message
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user, current_user
import datetime

from PhoenixNow.config import ProductionConfig

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/')
def home():
  form = CheckinForm()

  user = current_user

  return render_template('home.html', user=user, form=form)

@regular.route('/signup', methods=['GET', 'POST'])
@login_notrequired
def signup():

  form = SignupForm()
  
  if request.method == 'POST':
    if form.validate_on_submit():
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      token = generate_confirmation_token(newuser.email)
      confirm_url = url_for('regular.verify_email', token=token, _external=True)
      html = render_template('activate.html', confirm_url=confirm_url)
      subject = "Please confirm your email"
      #send_email(newuser.email, subject, html)
      flash('A verification email has been sent via email.', 'success')

      login_user(newuser)
      return redirect(url_for('regular.unverified'))

    else:   
      return render_template('signup.html', form=form)
   
  elif request.method == 'GET':
      return render_template('signup.html', form=form)

@regular.route('/signin', methods=['GET', 'POST'])
@login_notrequired
def signin():

  form = SigninForm()
  
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(email = form.email.data).first()
      login_user(user)
      return redirect(url_for('regular.home'))
    else:
      return render_template('signin.html', form=form)
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@regular.route('/signout')
@login_required
def signout():
  logout_user()
  return redirect(url_for('regular.home'))

@regular.route('/contact', methods=['GET','POST'])
@login_required
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate_on_submit():
      html = render_template("contact_email.html", name=form.name.data,
              email=form.email.data, message=form.message.data)
      subject = "PhoenixNow Contact: " + form.subject.data
      send_email("nick@nickendo.com", subject, html)
      flash('Your contact us email has been sent.', 'success')
      return render_template('contact.html', success=True)
    else:
      return render_template('contact.html', form=form)


  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@regular.route('/verify/<token>')
@login_required
@check_notverified
def verify_email(token):
  email = confirm_token(token)
  user = current_user
  if user.email == email:
    user.verified = True
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
  else:
    flash('The confirmation link is invalid or has expired.', 'danger')
  return redirect(url_for('regular.home'))

@regular.route('/unverified')
@login_required
@check_notverified
def unverified():
    flash('Please confirm your account!', 'warning')
    return render_template('unverified.html')

@regular.route('/resend')
@login_required
@check_notverified
def resend_verification():
    user = current_user
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('regular.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)
    flash('A new verification email has been sent.', 'success')
    return redirect(url_for('regular.unverified'))

@regular.route('/checkin')
@login_required
@check_verified
def checkin():
    user = current_user
    checkinObject = Checkin()
    user.checkins.append(checkinObject)
    db.session.add(checkinObject)
    user.checkedin = True
    db.session.commit()
    flash('Successfully checked in')
    return redirect(url_for('regular.home'))
