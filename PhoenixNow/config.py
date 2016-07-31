class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///data.db'

class DevelopmentConfig(Config):
    DEBUG = True
