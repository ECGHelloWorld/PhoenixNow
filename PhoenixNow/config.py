import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'idontknowwhatthisis'
    SECURITY_PASSWORD_SALT = "fortoken"
    MAIL_DEFAULT_SENDER = "support@phoenixnow.org"
    MAIL_SERVER = os.environ.get('EMAILSERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAILPASS')

class ProductionConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:pass@db/phoenixrises'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@db/postgres'
    CELERY_BROKER_URL = 'amqp://guest@rabbitmq//'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///file.db'
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
