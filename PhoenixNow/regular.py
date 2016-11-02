from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.user import create_user, checkin_user, reset_password_email, weekly_checkins
from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request, jsonify
from sqlalchemy.sql import func
from PhoenixNow.forms import SignupForm, SigninForm, ContactForm, CheckinForm, ScheduleForm, ResetForm, RequestResetForm, CalendarForm, EmailReminderForm
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.model import db, User, Checkin
from PhoenixNow.tasks import start_reminders, celery, count
from flask_login import login_required, login_user, logout_user, current_user
import datetime
import requests
from datetime import timedelta
import bcrypt
import json
import os

from PhoenixNow.config import ProductionConfig

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/beta')
@login_required
def beta():
    form = EmailReminderForm()
    user = current_user
    form.date.data = user.email_reminder
    form.enabled.data = True if len(user.email_reminder) > 0 else False
    return render_template('beta.html', form=form)

@regular.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
  user = current_user
  friend = User.query.filter_by(id=user_id).first_or_404()
  user.unfollow(friend)
  db.session.add(user)
  db.session.commit()
  flash('You have removed access from ' + friend.email)
  return redirect(url_for('regular.profile',user_id=user.id))

@regular.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
  user = current_user
  friend = User.query.filter_by(id=user_id).first_or_404()
  user.follow(friend)
  db.session.add(user)
  db.session.commit()
  flash('You given access to ' + friend.email)
  return redirect(url_for('regular.profile',user_id=user.id))

@regular.route('/unfollowall')
@login_required
def unfollowall():
  user = current_user
  profiles = User.query.all()
  for profile in profiles:
	user.unfollow(profile)
  db.session.add(user)
  db.session.commit()
  flash('You have removed access from everyone')
  return redirect(url_for('regular.profile',user_id=user.id))

@regular.route('/followall')
@login_required
def followall():
  user = current_user
  profiles = User.query.all()
  for profile in profiles:
	user.follow(profile)
  db.session.add(user)
  db.session.commit()
  flash('You have given access to everyone')
  return redirect(url_for('regular.profile',user_id=user.id))

@regular.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
  if request.method == 'POST':
    user = current_user
    return 'post sent'

  elif request.method == 'GET':
    user = current_user
    friend = User.query.filter_by(id=user_id).first_or_404()
    if friend.is_following(user) or friend.id == user.id:
	permission = True
    	return render_template('profile.html', friend=friend, user=user, permission=permission)
    else:
	permission = False
    	return render_template('profile.html', friend=friend, user=user, permission=permission)

@regular.route('/beta/reminder', methods=['POST'])
@login_required
def reminder():
    form = EmailReminderForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = current_user

        if form.enabled.data:
            # It doesn't matter if multiple reminders are created because 
            if len(user.email_reminder) == 0:
                flash("Email reminder time was set.")
            else:
                if len(user.email_reminder_id) > 0:
                    celery.control.revoke(user.email_reminder_id, terminate=True)
                    flash("Email reminder time was changed.")

            user.email_reminder = form.date.data
            start_reminders.delay(user.id)
        else:
            if len(user.email_reminder_id) > 0:
                celery.control.revoke(user.email_reminder_id, terminate=True)
            user.email_reminder = ""
            flash("Email reminder time was disabled.")


        db.session.commit()

        return redirect(url_for('regular.beta'))

@regular.route('/saveendpoint', methods=['POST'])
@login_required
def save_endpoint():
  data = request.json['endpoint']
  data = data.split('/')[-1]
  user = current_user
  user.gcm_endpoint = data
  db.session.commit()
  return jsonify({"title": data})

@regular.route('/sw.js')
def root():
    return regular.send_static_file('sw.js')

@regular.route('/notifications/beta')
@login_required
def notifications():
    user = current_user
    return render_template('notifications_beta.html',user=user)

@regular.route('/notifications/betatest')
@login_required
def notifications_test():
    user = current_user
    payload = {'registration_ids':[user.gcm_endpoint]}
    url = 'https://android.googleapis.com/gcm/send'
    headers = {"Authorization": "key=" + os.environ.get('TEMPAPIKEY'), "Content-Type":"application/json"}
    res = requests.post(url,headers=headers,data=json.dumps(payload))
    return res.content

@regular.route('/history', methods=['GET', 'POST'])
@login_required
def history():

  form = CalendarForm()
  user = current_user
  today = datetime.date.today()
  chart = False

  if request.method == 'POST':
      chart = True
      try:
        stringdate = form.date.data
        searchdate = datetime.datetime.strptime(stringdate, '%Y-%m-%d').date()
      except:
        return "Improper Date Format"

      if request.form['submit'] == "Next Week":
        searchdate = searchdate + timedelta(days=7)
        form.date.data = searchdate

      if request.form['submit'] == "Previous Week":
        searchdate = searchdate + timedelta(days=-7)
        form.date.data = searchdate

      user_week = weekly_checkins(searchdate, user)

      return render_template('history.html', user=user, user_week=user_week, searchdate=searchdate, form=form, chart=chart, today=today)
                 
  elif request.method == 'GET':
    return render_template('history.html', form=form, today=today)

@regular.route('/')
def home():
    form = CheckinForm()
    schedule_form = ScheduleForm()

    CheckinCount = Checkin.query.count()
    
    if not current_user.is_authenticated:
        return render_template('home.html', user=current_user,
                CheckinCount=CheckinCount)

    user = current_user

    today = datetime.date.today()
    
    checkin_today = Checkin.query.filter(Checkin.user==user,
            func.date(Checkin.checkin_timestamp)==today).first()

    if checkin_today is None:
        checkedin = False
    else:
        checkedin = True
    
    user_week = weekly_checkins(today, user)

    return render_template('home.html', user=user, form=form,
            checkedin=checkedin, schedule_form=schedule_form,
            user_week=user_week, today=today)

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
      send_email("chaudhryam@guilford.edu, helloworldappclub@gmail.com, kerrj@guilford.edu, nairv@guilford.edu, daynb@guilford.edu", subject, html)
      flash('Your contact us email has been sent.', 'success')
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

@regular.route('/about')
def about():
    return render_template('about.html')

#Code here for potential future schedule page if necessary
# @regular.route('/schedule')
# @login_required
# @check_verified
# def schedule():
#     user = current_user

