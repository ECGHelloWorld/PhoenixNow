from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String)
    salt = db.Column(db.String)
    signedin = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)
    signins = db.relationship('Signin', backref='user', lazy='dynamic')
    verified = db.Column(db.Boolean)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email
        self.salt = bcrypt.gensalt()
        self.pw_hash = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.timestamp = datetime.datetime.utcnow()
        self.signedin = False
        self.verified = False

    def check_password(self, password):
        return self.pw_hash == bcrypt.hashpw(password.encode('utf-8'), self.salt)

    def is_admin(self):
        if self.email == 'daynb@guilford.edu':
            return True
        elif self.email == 'kiddlm@guilford.edu':
            return True
        elif self.email=='kerrj@guilford.edu':
            return True
        elif self.email=='justin.g.kerr@gmail.com':
            return True
        else:
            return False

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_in = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Signin(id='%s')>" % (self.id)
