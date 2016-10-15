from PhoenixNow.mail import generate_confirmation_token, send_email
from flask import url_for, render_template
from PhoenixNow.model import db, User, Checkin
from PhoenixNow.week import Week
import datetime

def week_magic(day):
    day_of_week = day.weekday()

    to_beginning_of_week = datetime.timedelta(days=day_of_week)
    monday = day - to_beginning_of_week

    to_end_of_week = datetime.timedelta(days=4 - day_of_week)
    friday = day + to_end_of_week

    tuesday = day + datetime.timedelta(days=3 - day_of_week)
    wednesday = day + datetime.timedelta(days=2 - day_of_week)
    thursday = day + datetime.timedelta(days=1 - day_of_week)

    return [monday, tuesday, wednesday, thursday, friday]

def weekly_checkins(date, user):

    week = week_magic(date)
    
    checkins = Checkin.query.filter(Checkin.user==user, Checkin.checkin_timestamp>=week[0]).order_by('Checkin.checkin_timestamp')

    user_week = [False, False, False, False, False]

    for date in week:
        for checkin in checkins:
            if date == checkin.checkin_timestamp.date():
                user_week[date.weekday()] = True

    return user_week

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

def reset_password_email(email):
    token = generate_confirmation_token(email)
    reset_url = url_for('regular.reset_password', token=token, _external=True)
    html = render_template('resetemail.html', reset_url=reset_url)
    subject = "Password reset request."
    send_email(email, subject, html)
    return True

class get_weekly_checkins:
    
    def __init__(self, date): # creates a list of all checkins on each day of the week
        self.monday_checkins = Checkin.query.filter(Checkin.checkin_week == str(date.isocalendar()[1]), Checkin.checkin_day == str(1) ).all()
        self.tuesday_checkins = Checkin.query.filter(Checkin.checkin_week == str(date.isocalendar()[1]), Checkin.checkin_day == str(2) ).all()
        self.wednesday_checkins = Checkin.query.filter(Checkin.checkin_week == str(date.isocalendar()[1]), Checkin.checkin_day == str(3) ).all()
        self.thursday_checkins = Checkin.query.filter(Checkin.checkin_week == str(date.isocalendar()[1]), Checkin.checkin_day == str(4) ).all()
        self.friday_checkins = Checkin.query.filter(Checkin.checkin_week == str(date.isocalendar()[1]), Checkin.checkin_day == str(5) ).all()
   
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
        for checkin in self.tuesday_checkins:
            checkin.user.tuesday = "present"
        for checkin in self.wednesday_checkins:
            checkin.user.wednesday = "present"
        for checkin in self.thursday_checkins:
            checkin.user.thursday = "present"
        for checkin in self.friday_checkins:
            checkin.user.friday = "present"
        db.session.commit()
    def create_week_object(self, user):
        week = Week()
        for checkin in self.monday_checkins:
            if checkin.user_id == user.id:
              week.monday = "present"
        for checkin in self.tuesday_checkins:
            if checkin.user_id == user.id:
              week.tuesday = "present"
        for checkin in self.wednesday_checkins:
            if checkin.user_id == user.id:
              week.wednesday = "present"
        for checkin in self.thursday_checkins:
            if checkin.user_id == user.id:
              week.thursday = "present"
        for checkin in self.friday_checkins:
            if checkin.user_id == user.id:
              week.friday = "present"
        return week
