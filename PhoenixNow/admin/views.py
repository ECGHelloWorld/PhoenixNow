from flask import Flask, render_template, Blueprint
from PhoenixNow.regular.decorators import login_notrequired, admin_required, check_verified, check_notverified
from PhoenixNow.regular.model import db, User, Checkin
from flask_login import login_required, login_user, logout_user
from .forms import AdminForm

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
@admin_required
def home():
  form = AdminForm()
  return render_template('admin/home.html',form=form)

@admin.route('/database')
@login_required
@admin_required
def database():
  users = User.query.all()
  return render_template('admin/database.html',users=users)
