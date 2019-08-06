from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.user import create_user, checkin_user, reset_password_email, weekly_checkins, monthly_checkins
from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from PhoenixNow.forms import SignupForm, SigninForm, ContactForm, CheckinForm, ScheduleForm, ResetForm, RequestResetForm, CalendarForm, EmailReminderForm
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user, current_user
import datetime
import requests
import calendar
from datetime import timedelta
import bcrypt
import json
import os

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/history')
@regular.route('/history/<int:month_num>')
@login_required
def history(month_num=None):
  user = current_user
  today = datetime.date.today()
  if month_num is None:
    if today.month > 1:
      prev_month = today.month - 1
    else:
      prev_month = 12

    if today.month < 12:
      next_month = today.month + 1
    else:
      next_month = 1

    month = monthly_checkins(today.year, today.month, user)
    month_range = calendar.monthrange(today.year, today.month)
    month_name = datetime.date(today.year, today.month, 1).strftime("%B")
  else:
    if month_num > 12:
      month_num = 1
    elif month_num < 1:
      month_num = 12

    if month_num > 1:
      prev_month = month_num - 1
    else:
      prev_month = 12

    if month_num < 12:
      next_month = month_num + 1
    else:
      next_month = 1

    month = monthly_checkins(today.year, month_num, user)
    month_range = calendar.monthrange(today.year, month_num)
    month_name = datetime.date(today.year, month_num, 1).strftime("%B")

  return render_template('history.html', user=user, start_day=month_range[0], month_name=month_name, next_month=next_month, prev_month=prev_month, month=month)

@regular.route('/')
def home():
    user = current_user

    CheckinCount = Checkin.query.count()

    if not current_user.is_authenticated:
        return render_template('unauthenticated-home.html', user=current_user,
                CheckinCount=CheckinCount)

    if not user.verified:
      return redirect(url_for('regular.unverified'))
    
    today = datetime.date.today()
    
    checkin_today = Checkin.query.filter(Checkin.user==user,
            func.date(Checkin.checkin_timestamp)==today).first()

    if request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr

    if checkin_today is None:
        checkedin = False
        if ip.rsplit('.',1)[0] in ['192.154.63']:
          if checkin_user(user):
              checkedin = True
        else:
            flash("We couldn't check you in. :( Are you on the Guilford network?")
    else:
        checkedin = True

    user_week = weekly_checkins(today, user)

    return render_template('home.html', user=user, checkedin=checkedin, user_week=user_week, today=today)

@regular.route('/signup', methods=['GET', 'POST'])
@login_notrequired
def signup():

  form = SignupForm()
  
  if request.method == 'POST':
    if form.validate_on_submit():
      user = create_user(form.firstname.data, form.lastname.data, form.grade.data, form.email.data, form.password.data)
      login_user(user,remember=True)

      flash('A verification email has been sent via email.', 'success')
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
      user = User.query.filter_by(email = form.email.data.lower()).first()
      login_user(user,remember=True)
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
      send_email("phoenixnow@guilford.edu", subject, html)
      return render_template('contact.html', success=True)
    else:
      return render_template('contact.html', form=form)


  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@regular.route('/verify/<token>')
def verify_email(token):

  tokenemail = confirm_token(token)
  if tokenemail is False:
    flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('regular.home'))

  user = User.query.filter_by(email = tokenemail).first()
  if user:
    user.verified = True
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
  else:
    flash('The confirmation link is invalid or has expired.', 'danger')
  return redirect(url_for('regular.home'))

@regular.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
  form = ResetForm()

  tokenemail = confirm_token(token)
  if tokenemail is False:
    flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('regular.home'))

  user = User.query.filter_by(email = tokenemail).first()
  if user:
    if request.method == 'POST':
      if form.validate_on_submit():
        user.pw_hash = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.session.commit()
        login_user(user,remember=True)
        flash('Your password has been reset.')
        return redirect(url_for('regular.home'))
      else:
        return render_template('reset.html', form=form, token=token)
    elif request.method == 'GET':
      return render_template('reset.html', form=form, token=token)
  else:
    flash('The confirmation link is invalid or has expired.', 'danger')

@regular.route('/requestreset', methods=['GET', 'POST'])
def requestreset():
  form = RequestResetForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      reset_password_email(form.email.data)
      flash('An email has been sent to reset your password.')
      return redirect(url_for('regular.home'))
    else:
      return render_template('requestreset.html', form=form)
  elif request.method == 'GET':
    return render_template('requestreset.html', form=form)

@regular.route('/unverified')
@login_required
@check_notverified
def unverified():
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

@regular.route('/about')
def about():
    return render_template('about.html')