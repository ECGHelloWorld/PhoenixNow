# celery -A celery_manager worker -B
from celery import Celery
from celery.schedules import crontab
from PhoenixNow.model import User, db

BACKEND_URL = 'db+sqlite:///celery.db'

app = Celery('tasks', backend=BACKEND_URL, broker='amqp://localhost')

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        # Resets signins at 7am EDT everyday
        'reset-signins-every-day': {
            'task': 'tasks.reset_signins',
            'schedule': crontab(minute=0, hour=11)
        }
    },
    CELERY_TIMEZONE = 'UTC'
)

@app.task
def reset_signins():
    users = User.query.all()
    for user in users:
        user.checkedin = False
    db.session.commit()
