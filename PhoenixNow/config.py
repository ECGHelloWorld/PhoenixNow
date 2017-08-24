import os

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRETKEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITYSALT')
    MAIL_DEFAULT_SENDER = "support@phoenixnow.org"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SERVER = os.environ.get('EMAILSERVER')
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAILPASS')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data.db'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False