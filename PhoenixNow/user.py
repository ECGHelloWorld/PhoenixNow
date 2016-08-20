from PhoenixNow.mail import generate_confirmation_token, send_email
from flask import url_for, render_template
from PhoenixNow.model import db, User, Checkin
import datetime

def create_user(first, last, grade, email, password):
    newuser = User(first, last, grade, email, password)
    db.session.add(newuser)
    db.session.commit()
    token = generate_confirmation_token(newuser.email)
    confirm_url = url_for('regular.verify_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(newuser.email, subject, html)
    return newuser

def checkin_user(user):
    today = datetime.date.today()
    for checkin in user.checkins:
        if checkin.checkin_timestamp.date() == today:
            return False
    checkinObject = Checkin()
    user.checkins.append(checkinObject)
    db.session.add(checkinObject)
    user.checkedin = True
    db.session.commit()
    return True

class get_weekly_checkins:
    
    def __init__(self, date): # creates a list of all checkins on each day of the week
        self.monday_checkins = Checkin.query.filter(Checkin.checkin_week == date.isocalendar()[1], Checkin.checkin_day == 1 ).all()
        self.tuesday_checkins = Checkin.query.filter(Checkin.checkin_week == date.isocalendar()[1], Checkin.checkin_day == 2 ).all()
        self.wednesday_checkins = Checkin.query.filter(Checkin.checkin_week == date.isocalendar()[1], Checkin.checkin_day == 3 ).all()
        self.thursday_checkins = Checkin.query.filter(Checkin.checkin_week == date.isocalendar()[1], Checkin.checkin_day == 4 ).all()
        self.friday_checkins = Checkin.query.filter(Checkin.checkin_week == '33', Checkin.checkin_day == '5' ).all()
   
    def update_database(self): # change the day values to True if a checkin exists
        users = User.query.all()
        for user in users:
            user.monday = "" #WITHOUT THIS IT GIVES 'VARCHARS' WHEN EMPTY OR SOMETHING??//
            user.tuesday = ""
            user.wednesday = ""
            user.thursday = ""
            user.friday = ""
        for checkin in self.monday_checkins:
            checkin.user.monday = "present"
            db.session.commit()
        for checkin in self.tuesday_checkins:
            checkin.user.tuesday = "present"
            db.session.commit()
        for checkin in self.wednesday_checkins:
            checkin.user.wednesday = "present"
            db.session.commit()
        for checkin in self.thursday_checkins:
            checkin.user.thursday = "present"
            db.session.commit()
        for checkin in self.friday_checkins:
            checkin.user.friday = "present"
            db.session.commit()
