from flask_mail import Mail, Message
from PhoenixNow.config import ProductionConfig

mail = Mail()

from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(ProductionConfig.SECRET_KEY)
    return serializer.dumps(email, salt=ProductionConfig.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(ProductionConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=ProductionConfig.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=to.split(", "),
        html=template,
        sender=ProductionConfig.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)
