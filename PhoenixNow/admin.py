from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from datetime import timedelta
from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.model import db, User, Checkin
from PhoenixNow.user import get_weekly_checkins, admin_weekly_checkins
from flask_login import login_required, login_user, logout_user
from PhoenixNow.forms import UserForm, CalendarForm, ScheduleForm
import datetime
import requests
import json
import os

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/grade/<int:grade>', methods=['GET', 'POST'])
@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def home(grade=None):
    form = CalendarForm()
    if request.method == 'POST':
        try:
            stringdate = form.date.data
            searchdate = datetime.datetime.strptime(stringdate, '%Y-%m-%d').date()
        except:
            return "Improper Date Format" + form.date.data

        if request.form['submit'] == "Next Week":
            searchdate = searchdate + timedelta(days=7)
            form.date.data = searchdate

        if request.form['submit'] == "Previous Week":
            searchdate = searchdate + timedelta(days=-7)
            form.date.data = searchdate

    if request.method == 'GET':
        searchdate = datetime.date.today()
    
    if grade is None:
      users = User.query.all()
    else:
      users = User.query.filter_by(grade=grade).all()

    users.sort(key=lambda user: (user.grade, user.lastname)) # sort by grade and name
    weekly_checkins = admin_weekly_checkins(searchdate, grade)
    for checkin in weekly_checkins:
      day = checkin.checkin_timestamp.strftime("%A")
      if day == 'Monday':
        checkin.user.monday = "present"
      elif day == 'Tuesday':
        checkin.user.tuesday = "present"
      elif day == 'Wednesday':
        checkin.user.wednesday = "present"
      elif day == 'Thursday':
        checkin.user.thursday = 'present'
      elif day == 'Friday':
        checkin.user.friday = 'present'
    return render_template('admin.html', searchdate=searchdate, grade=grade, form=form, users=users, checkins=weekly_checkins)

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
  
  form = UserForm()
  schedule_form = ScheduleForm()

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
    return render_template('user.html', schedule_form=schedule_form, user=user, form=form)

@admin.route('/user/<int:user_id>/schedule', methods=['POST'])
@login_required
@admin_required
def schedule(user_id):
    form = ScheduleForm()

    user = User.query.filter_by(id=user_id).first_or_404()

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

    return redirect(url_for('admin.user', user_id=user_id))