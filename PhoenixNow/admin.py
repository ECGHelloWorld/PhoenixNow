from flask import Flask, render_template, Blueprint
from PhoenixNow.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
@admin_required
def home():
  users = User.query.all()
  return render_template('admin.html', users=users)
