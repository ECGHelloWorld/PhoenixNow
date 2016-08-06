class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = 'idontknowwhatthisis'
    SECURITY_PASSWORD_SALT = "fortoken"
    MAIL_DEFAULT_SENDER = "support@chadali.me"

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///data.db'

class DevelopmentConfig(Config):
    DEBUG = True
