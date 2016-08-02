from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.validators import InputRequired, Email

class SignupForm(Form):
  firstname = StringField("First Name",  [InputRequired("Please enter your first name.")])
  lastname = StringField("Last Name",  [InputRequired("Please enter your last name.")])
  email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
  password = PasswordField('Password', [InputRequired("Please enter a password.")])
  submit = SubmitField("Create account")

class SigninForm(Form):
  email = StringField("Email",  [InputRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', [InputRequired("Please enter a password.")])
  submit = SubmitField("Sign In")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

