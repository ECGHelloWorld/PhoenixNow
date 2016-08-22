from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    grade = db.Column(db.Integer)
    pw_hash = db.Column(db.String)
    salt = db.Column(db.String)
    checkedin = db.Column(db.Boolean)
    creation_timestamp = db.Column(db.DateTime)
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')
    verified = db.Column(db.Boolean)
    schedule_verified = db.Column(db.Boolean)
    schedule = db.Column(db.String)
    schedule_monday = db.Column(db.Boolean)
    schedule_tuesday = db.Column(db.Boolean)
    schedule_wednesday = db.Column(db.Boolean)
    schedule_thursday = db.Column(db.Boolean)
    schedule_friday = db.Column(db.Boolean)
    monday = db.Column(db.String)
    tuesday = db.Column(db.String)
    wednesday = db.Column(db.String)
    thursday = db.Column(db.String)
    friday = db.Column(db.String)

    def __init__(self, firstname, lastname, grade, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email
        self.grade = grade
        self.salt = bcrypt.gensalt()
        self.pw_hash = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.creation_timestamp = datetime.datetime.utcnow()
        self.checkedin = False
        self.verified = False
        self.schedule_verified = False
        self.schedule = "null"
        self.schedule_monday = True
        self.schedule_tuesday = True
        self.schedule_wednesday = True
        self.schedule_thursday = True
        self.schedule_friday = True
        self.monday = ""
        self.tuesday = ""
        self.wednesday = ""
        self.thursday = ""
        self.friday = ""

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_authenticated(self):
        """Return True if the user is verified."""
        return self.verified

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def check_password(self, password):
        return self.pw_hash == bcrypt.hashpw(password.encode('utf-8'), self.salt)

    def is_admin(self):
        if self.email in ['chaudhryam@guilford.edu', 'daynb@guilford.edu', 'admin@phoenixnow.me', 'kiddlm@guilford.edu', 'websternb@guilford.edu', 'lkiser@guilford.edu']:
          return True
        else:
          return False

    def __repr__(self):
        return repr((self.lastname))

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_timestamp = db.Column(db.DateTime)
    checkin_week = db.Column(db.String)
    checkin_day = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self):
      self.checkin_timestamp = datetime.datetime.utcnow()
      self.checkin_week = datetime.date.today().isocalendar()[1]
      self.checkin_day = datetime.date.today().isocalendar()[2]

    def __repr__(self):
        return "<Checkin(id='%s')>" % (self.id)
