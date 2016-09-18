from PhoenixNow.factory import create_celery_app
from PhoenixNow.model import User
from PhoenixNow.mail import send_email, mail
from flask import render_template
from celery import Celery
import datetime

celery = create_celery_app()
#celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def remind(userid):
    user = User.query.get(userid)
    body = render_template("reminder_email.html", name=user.firstname)
    send_email(user.email, "Checkin " + datetime.date.today().strftime('%x'), body)
    remind.apply_async([userid], countdown=30)
    return user.email + " " + user.firstname

@celery.task
def hi():
    return "hi"
