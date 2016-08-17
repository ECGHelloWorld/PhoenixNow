from flask import Flask, render_template, Blueprint, redirect, url_for, flash
from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
@admin_required
def home():
  users = User.query.all()
  checkins = Checkin.query.all()
  return render_template('admin.html', users=users)

@admin.route('/user/<int:user_id>')
@login_required
@admin_required
def user(user_id):
  user = User.query.filter_by(id=user_id).first_or_404()
  return render_template('user.html', user=user)

@admin.route('/user/<int:user_id>/verify_schedule')
@login_required
@admin_required
def verify_schedule(user_id):
  verify_user = User.query.filter_by(id=user_id).first_or_404()
  verify_user.schedule_verified = not verify_user.schedule_verified
  db.session.commit()
  flash("User schedule verified")
  return redirect(url_for('admin.user', user_id=user_id))
