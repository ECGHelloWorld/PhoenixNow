from itsdangerous import URLSafeTimedSerializer

#from PhoenixNow import app
#https://realpython.com/blog/python/handling-email-confirmation-in-flask/


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer("SECRET KEY")
    return serializer.dumps(email, salt="SECRET PASSWORD SALT")


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer("SECRET KEY")
    try:
        email = serializer.loads(
            token,
            salt="SECRET PASSWORD SALT",
            max_age=expiration
        )
    except:
        return False
    return email
