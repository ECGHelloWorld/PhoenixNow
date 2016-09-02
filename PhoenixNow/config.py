class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'idontknowwhatthisis'
    SECURITY_PASSWORD_SALT = "fortoken"
    MAIL_DEFAULT_SENDER = "support@chadali.me"

class ProductionConfig(Config):
#    SQLALCHEMY_DATABASE_URI = 'mysql+oursql://user:pass@localhost/dbname'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file.db'

class DevelopmentConfig(Config):
    DEBUG = True
