from .decorators import login_required, login_notrequired, admin_required, check_verified, check_notverified
from flask import Flask, render_template, request, flash, session, redirect, url_for
from .forms import SignupForm, SigninForm, ContactForm, CheckinForm
from .token import generate_confirmation_token, confirm_token
from flask_mail import Message, Mail
from .email import send_email
from .model import db, User, Checkin
from flask import Blueprint
import datetime

from PhoenixNow.config import ProductionConfig

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

mail = Mail()


@regular.route('/')
def home():
    return render_template('home.html')

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
      confirm_url = url_for('.verify_email', token=token, _external=True)
      html = render_template('activate.html', confirm_url=confirm_url)
      subject = "Please confirm your email"
      send_email(newuser.email, subject, html)
      flash('A verification email has been sent via email.', 'success')

      session['email'] = newuser.email
      return redirect(url_for('.unverified'))

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
      session['email'] = form.email.data.lower()
      return redirect(url_for('.profile'))
    else:
      return render_template('signin.html', form=form)
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@regular.route('/profile')
@login_required
def profile():
  form = CheckinForm()

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    session.pop('email', None)
    return redirect(url_for('.signin'))
  else:
    return render_template('profile.html', user=user, form=form)

@regular.route('/signout')
@login_required
def signout():
     
  session.pop('email', None)
  return redirect(url_for('.home'))

@regular.route('/admin')
@login_required
@admin_required
def admin():
  users = User.query.all()
  return render_template('admin.html', users=users)

@regular.route('/contact', methods=['GET','POST'])
@login_required
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate_on_submit():
      msg = Message(form.subject.data, sender='support@chadali.me', recipients=['chaudhryam@guilford.edu'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
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
  user = User.query.filter_by(email = session['email']).first_or_404()
  if user.email == email:
    user.verified = True
    #db.session.add(user)
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
  else:
    flash('The confirmation link is invalid or has expired.', 'danger')
  return redirect(url_for('.profile'))

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
    user = User.query.filter_by(email = session['email']).first()
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)
    flash('A new verification email has been sent.', 'success')
    return redirect(url_for('.unverified'))

@regular.route('/checkin')
@login_required
@check_verified
def checkin():
    user = User.query.filter_by(email = session['email']).first()
    checkinObject = Checkin()
    user.checkins.append(checkinObject)
    db.session.add(checkinObject)
    user.checkedin = True
    db.session.commit()
    flash('successfully checked in')
    return redirect(url_for('.profile'))

### test pages ###

@regular.route('/test')
def test():
    newuser = User("Admin", "Account", "23alic@gmail.com", "1")
    newuser1 = User("test", "Account", "1@gmail.com", "1")
    newuser2 = User("test", "Account", "2@gmail.com", "1")
    db.session.add(newuser)
    db.session.add(newuser1)
    db.session.add(newuser2)
    newuser.verified = True
    newuser1.verified = True
    newuser2.verified = True
    db.session.commit()
    session['email'] = "23alic@gmail.com"
    return redirect(url_for('.profile'))
