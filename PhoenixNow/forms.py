from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.validators import InputRequired, Email
from .model import db, User


class SignupForm(Form):
  firstname = StringField("First Name",  [InputRequired("Please enter your first name.")])
  lastname = StringField("Last Name",  [InputRequired("Please enter your last name.")])
  email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
  password = PasswordField('Password', [InputRequired("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = StringField("Email",  [InputRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', [InputRequired("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class ContactForm(Form):
  name = StringField("Name",  [InputRequired("Please enter your name.")])
  email = StringField("Your Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
  subject = StringField("Subject",  [InputRequired("Please enter a subject.")])
  message = TextAreaField("Message",  [InputRequired("Please enter a message.")])
  submit = SubmitField("Send")

class CheckinForm(Form):
  submit = SubmitField("Check in for the day.")
