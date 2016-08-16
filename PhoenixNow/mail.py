from flask_mail import Mail

mail = Mail()

from itsdangerous import URLSafeTimedSerializer
from PhoenixNow.config import ProductionConfig

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
