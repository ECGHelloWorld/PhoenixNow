from flask import Blueprint
from flask import Flask, render_template, request, flash, session, redirect, url_for
from .forms import SignupForm, SigninForm

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/')
def home():
    return render_template('home.html')

@regular.route('/hello')
def hello():
    """
    Example endpoint

    Returns "hello"
    """
    return "hello"

@regular.route('/signup', methods=['GET', 'POST'])
def signup():

  form = SignupForm()
 
  if 'email' in session:
      return redirect(url_for('.profile'))
  
  if request.method == 'POST':
    if form.validate_on_submit():
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('profile'))

    else:   
      return render_template('signup.html', form=form)
   
  elif request.method == 'GET':
      return render_template('signup.html', form=form)

@regular.route('/signin', methods=['GET', 'POST'])
def signin():

  form = SigninForm()
 
  if 'email' in session:
      return redirect(url_for('.profile'))
  
  if request.method == 'POST':
    if form.validate_on_submit():
      session['email'] = form.email.data
      return redirect(url_for('profile'))
    else:
      return render_template('signin.html', form=form)
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)
