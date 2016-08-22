from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.user import create_user, checkin_user, get_weekly_checkins, reset_password_email
from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request
from PhoenixNow.forms import SignupForm, SigninForm, ContactForm, CheckinForm, ScheduleForm, ResetForm, RequestResetForm
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user, current_user
import datetime
import bcrypt

from PhoenixNow.config import ProductionConfig

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/')
def home():
  form = CheckinForm()
  schedule_form = ScheduleForm()

  user = current_user

  if user.is_active:
    checkedin = False
    today = datetime.date.today()
    for checkin in user.checkins:
        if checkin.checkin_timestamp.date() == today:
            checkedin = True
    weekly_checkins = get_weekly_checkins(today) # look at user.py
    weekly_checkins.update_database() # look at user.py
    return render_template('home.html', user=user, form=form, schedule_form=schedule_form,checkedin=checkedin,today=today)

  return render_template('home.html', user=user, form=form, schedule_form=schedule_form)

@regular.route('/schedule', methods=['POST'])
@login_required
def schedule():
    form = ScheduleForm()

    user = current_user

    if form.validate_on_submit():
        user.schedule = ""
        user.schedule_monday = False
        user.schedule_tuesday = False
        user.schedule_wednesday = False
        user.schedule_thursday = False
        user.schedule_friday = False
        if form.monday.data:
            user.schedule = "M"
            user.schedule_monday = True
        if form.tuesday.data:
            user.schedule = "%s:T" % (user.schedule)
            user.schedule_tuesday = True
        if form.wednesday.data:
            user.schedule = "%s:W" % (user.schedule)
            user.schedule_wednesday = True
        if form.thursday.data:
            user.schedule = "%s:R" % (user.schedule)
            user.schedule_thursday = True
        if form.friday.data:
            user.schedule = "%s:F" % (user.schedule)
            user.schedule_friday = True
        if user.schedule == "M:T:W:R:F":
            user.schedule_verified = True
        else:
            user.schedule_verified = False
        db.session.commit()
        flash("Your schedule has been updated.")

    return redirect(url_for('regular.home'))

@regular.route('/signup', methods=['GET', 'POST'])
@login_notrequired
def signup():

  form = SignupForm()
  
  if request.method == 'POST':
    if form.validate_on_submit():
      user = create_user(form.firstname.data, form.lastname.data, form.grade.data, form.email.data, form.password.data)
      login_user(user)

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
      send_email("helloworldappclub@gmail.com", subject, html)
      flash('Your contact us email has been sent.', 'success')
      return render_template('contact.html', success=True)
    else:
      return render_template('contact.html', form=form)


  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@regular.route('/verify/<token>')
def verify_email(token):
  tokenemail = confirm_token(token)
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
  user = User.query.filter_by(email = tokenemail).first()
  if user:
    if request.method == 'POST':
      if form.validate_on_submit():
        user.pw_hash = bcrypt.hashpw(form.password.data.encode('utf-8'), user.salt)
        db.session.commit()
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
    if request.remote_addr.rsplit('.',1)[0] in ['192.154.63']:
        if checkin_user(user):
            flash('Successful Check-in!')
        else:
            flash('You are already signed in for today.')
    else:
        flash("Unsuccesful Check-in. Please check that you are on the Guilford College network.")
    return redirect(url_for('regular.home'))

#Code here for potential future schedule page if necessary
# @regular.route('/schedule')
# @login_required
# @check_verified
# def schedule():
#     user = current_user

