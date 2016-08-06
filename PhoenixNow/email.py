from PhoenixNow.config import ProductionConfig
from flask_mail import Message, Mail

mail = Mail()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=ProductionConfig.MAIL_DEFAULT_SENDER

    )
    mail.send(msg)
