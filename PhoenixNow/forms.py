from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email
from PhoenixNow.model import db, User


class SignupForm(Form):
  firstname = StringField("First Name",  [InputRequired("Please Enter Your First Name")])
  lastname = StringField("Last Name",  [InputRequired("Please Enter Your Last Name")])
  grade = StringField("Grade Level", [InputRequired("Please Enter Your Grade Level")])
  email = StringField("Email",  [InputRequired("Please Enter Your Email Address"), Email("This Field Requires a Valid Email Address")])
  password = PasswordField('Password', [InputRequired("Please Enter a Password")])
  confirmpassword = PasswordField('Confirm Password', [InputRequired("Please Repeat your Password")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
    
    domain = self.email.data.lower().split('@')[1]
    if domain != "guilford.edu":
      self.email.errors.append("Must Register With Guilford.edu Email")
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("This Email Is Already Taken")
      return False

    if self.password.data == self.confirmpassword.data:
      return True
    else:
      self.password.errors.append("Passwords Don't Match")
      return False

class SigninForm(Form):
  email = StringField("Email",  [InputRequired("Please Enter Your Email Address"), Email("Please Enter Your Email Address")])
  password = PasswordField('Password', [InputRequired("Please Enter a Password.")])
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
      self.email.errors.append("Invalid E-mail or Password")
      return False

class ResetForm(Form):
  password = PasswordField('Password', [InputRequired("Please Enter a Password.")])
  confirmpassword = PasswordField('Confirm Password', [InputRequired("Please Enter a Password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
    if self.password.data == self.confirmpassword.data:
      return True
    else:
      self.password.errors.append("Passwords Don't Match")
      return False

class RequestResetForm(Form):
  email = StringField("Email",  [InputRequired("Please Enter Your Email Address"), Email("Please Enter Your Email Address")])
  submit = SubmitField("Submit")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      return True
    else:
      self.email.errors.append("This Email Does Not Exist")
      return False

class ContactForm(Form):
  name = StringField("Name",  [InputRequired("Please Enter Your Name")])
  email = StringField("Your Email",  [InputRequired("Please Enter Your Email Address."), Email("This Field Requires a Valid Email Address")])
  subject = StringField("Subject",  [InputRequired("Please Enter a Subject")])
  message = TextAreaField("Message",  [InputRequired("Please Enter a Message")])
  submit = SubmitField("Send")

class CheckinForm(Form):
  checkin = SubmitField("Check-in Today")

class ScheduleForm(Form):
  monday = BooleanField("Monday")
  tuesday = BooleanField("Tuesday")
  wednesday = BooleanField("Wednesday")
  thursday = BooleanField("Thursday")
  friday = BooleanField("Friday")
  submit = SubmitField("Submit")
