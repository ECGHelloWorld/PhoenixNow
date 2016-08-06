from flask_mail import Message, Mail

mail = Mail()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        #sender=app.config['MAIL_DEFAULT_SENDER']
	sender="support@chadali.me"
    )
    mail.send(msg)
