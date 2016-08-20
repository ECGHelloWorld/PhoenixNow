from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.user import create_user, checkin_user
from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, request
from PhoenixNow.forms import SignupForm, SigninForm, ContactForm, CheckinForm, ScheduleForm
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user, current_user
import datetime

from PhoenixNow.config import ProductionConfig

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/test')
def test():
  user = create_user("johnny", "boy", "11", "1@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  user = create_user("johnny", "lad", "12", "2@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  user = create_user("johnny", "apple", "9", "3@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  user = create_user("johnny", "zoo", "10", "4@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  user = user = create_user("johnny", "quill", "11", "5@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  user = create_user("admin", "account", "11", "chaudhryam@guilford.edu", "1")
  checkin_user(user)
  user.verified = True
  db.session.commit()
  return redirect(url_for('regular.home'))

@regular.route('/')
def home():
  form = CheckinForm()
  schedule_form = ScheduleForm()

  user = current_user

  if user.is_active:
    today = datetime.date.today()
    for checkin in user.checkins:
        if checkin.checkin_timestamp.date() == today:
            checkedin = True
        return render_template('home.html', user=user, form=form, schedule_form=schedule_form,checkedin=checkedin,today=today)

  return render_template('home.html', user=user, form=form, schedule_form=schedule_form)

@regular.route('/schedule', methods=['POST'])
@login_required
def schedule():
    form = ScheduleForm()

    user = current_user

    if form.validate_on_submit():
        user.schedule = ""
        user.schedule_verified = False
        if form.monday.data:
            user.schedule = "M"
        if form.tuesday.data:
            user.schedule = "%s:T" % (user.schedule)
        if form.wednesday.data:
            user.schedule = "%s:W" % (user.schedule)
        if form.thursday.data:
            user.schedule = "%s:R" % (user.schedule)
        if form.friday.data:
            user.schedule = "%s:F" % (user.schedule)
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
      send_email("nick@nickendo.com", subject, html)
      flash('Your contact us email has been sent.', 'success')
      return render_template('contact.html', success=True)
    else:
      return render_template('contact.html', form=form)


  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@regular.route('/verify/<token>')
def verify_email(token):
  tokenemail = confirm_token(token)
  user = User.query.filter_by(email = tokenemail).first_or_404()
  if user:
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
    if request.remote_addr in ['192.168.1.1', '192.168.1.2']:
        if checkin_user(user):
            flash('Successfully checked in')
        else:
            flash('Unsuccessful, already checked in for today')
    else:
        flash("You're not on the Guilford network")
    return redirect(url_for('regular.home'))
