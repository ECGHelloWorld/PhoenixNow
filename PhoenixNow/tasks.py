from PhoenixNow.factory import create_celery_app
from PhoenixNow.model import User, db
from PhoenixNow.mail import send_email, mail
from flask import render_template
from celery import Celery, uuid
import time
import datetime

celery = create_celery_app()
#celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def count():
    return "hiii"

@celery.task
def remind(userid):
    user = User.query.get(userid)

    if len(user.email_reminder) == 0:
        return

    now = datetime.datetime.now()

    today = datetime.date.today()

    tomorrow = today + datetime.timedelta(days=1)
    next_time = datetime.datetime.combine(tomorrow,
            datetime.datetime.strptime(user.email_reminder, "%H:%M").time())

    seconds = next_time - now
    seconds = seconds.total_seconds()

    body = render_template("reminder_email.html", name=user.firstname)
    send_email(user.email, "Checkin " + datetime.date.today().strftime('%x'), body)

    task_id = uuid()

    if len(user.email_reminder_id) > 0:
        celery.control.revoke(user.email_reminder_id, terminate=True)

    user.email_reminder_id = task_id
    db.session.commit()

    remind.apply_async([userid], task_id=task_id, countdown=seconds)
    return user.email + " " + user.firstname

# This is needed b/c we don't have an eta the first time we start the task
@celery.task
def start_reminders(userid):
    user = User.query.get(userid)

    if len(user.email_reminder) == 0:
        return

    now = datetime.datetime.now()

    today = datetime.date.today()

    potential_time = datetime.datetime.combine(today, datetime.datetime.strptime(user.email_reminder,
        "%H:%M").time())

    # If the time hasn't happened yet today, send a reminder that day
    # otherwise schedule it for tomorrow
    if now > potential_time:
        tomorrow = today + datetime.timedelta(days=1)
        next_time = datetime.datetime.combine(tomorrow,
                datetime.datetime.strptime(user.email_reminder, "%H:%M").time())
        time_to_send = next_time
    else:
        time_to_send = potential_time

    seconds = time_to_send - now
    seconds = seconds.total_seconds()

    if len(user.email_reminder_id) > 0:
        celery.control.revoke(user.email_reminder_id, terminate=True)

    task_id = uuid()
    user.email_reminder_id = task_id

    db.session.commit()

    remind.apply_async([userid], task_id=task_id, countdown=seconds)

    return "reminder started"
