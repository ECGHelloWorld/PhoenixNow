from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.model import db, User, Checkin
from PhoenixNow.user import get_weekly_checkins
from flask_login import login_required, login_user, logout_user
from PhoenixNow.forms import UserForm
import datetime

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
@admin_required
def home():
    users = User.query.all()
    users.sort(key=lambda user: (user.grade, user.lastname)) # sort by grade and name
    checkins = Checkin.query.filter(Checkin.checkin_timestamp >= datetime.date.today()).all()
    checkins.sort(key=lambda checkin: (checkin.user.lastname)) # sort by grade and name
    today = datetime.date.today()
    weekly_checkins = get_weekly_checkins(today) # look at user.py
    weekly_checkins.update_database() # look at user.py
    return render_template('admin.html', users=users, checkins=checkins)

@admin.route('/push')
@login_required
@admin_required
def push():
    users = User.query.all()
    users.sort(key=lambda user: (user.grade, user.lastname)) # sort by grade and name
    return render_template('push.html', users=users)

@admin.route('/sendpush/<str:gcm_endpoint>', methods=['GET', 'POST'])
@login_required
@admin_required
def sendpush(gcm_endpoint):
  if request.method == 'POST':
    payload = {'registration_ids':[gcm_endpoint]}
    url = 'https://android.googleapis.com/gcm/send'
    headers = {"Authorization": "key=" + os.environ.get('TEMPAPIKEY'), "Content-Type":"application/json"}
    res = requests.post(url,headers=headers,data=json.dumps(payload))
    return res.content

  elif request.method == 'GET':
    payload = {'registration_ids':[gcm_endpoint]}
    url = 'https://android.googleapis.com/gcm/send'
    headers = {"Authorization": "key=" + os.environ.get('TEMPAPIKEY'), "Content-Type":"application/json"}
    res = requests.post(url,headers=headers,data=json.dumps(payload))
    return res.content

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
  
  form = UserForm()

  if request.method == 'POST':
    user = User.query.filter_by(id=user_id).first_or_404()
    if form.firstname.data:
      user.firstname = form.firstname.data
    if form.lastname.data:
      user.lastname = form.lastname.data
    if form.grade.data:
      user.grade = form.grade.data
    db.session.commit()
    return redirect(url_for('admin.user', user_id=user_id))

  elif request.method == 'GET':
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user.html', user=user, form=form)

@admin.route('/user/<int:user_id>/verify_schedule')
@login_required
@admin_required
def verify_schedule(user_id):
  verify_user = User.query.filter_by(id=user_id).first_or_404()
  verify_user.schedule_verified = not verify_user.schedule_verified
  db.session.commit()
  flash("User schedule verified")
  return redirect(url_for('admin.user', user_id=user_id))

@admin.route('/grade/<int:grade>')
@login_required
@admin_required
def grade(grade):
  users = User.query.filter_by(grade=grade).all()
  users.sort(key=lambda user: user.lastname) # sort by last name
  checkins = Checkin.query.filter(Checkin.checkin_timestamp >=
          datetime.date.today(), Checkin.user.has(grade=grade)).all()
  checkins.sort(key=lambda checkin: (checkin.user.lastname)) # sort by grade and name
  today = datetime.date.today()
  weekly_checkins = get_weekly_checkins(today) # look at user.py
  weekly_checkins.update_database() # look at user.py
  return render_template('grade.html', users=users,user=user,checkins=checkins,grade=grade)
