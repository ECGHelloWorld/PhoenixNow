from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, StringField, PasswordField
from wtforms.validators import InputRequired, Email

class AdminForm(Form):
  database = SubmitField("See visual database.")
