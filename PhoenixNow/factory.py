from PhoenixNow.config import DevelopmentConfig, ProductionConfig
from PhoenixNow.mail import mail
from PhoenixNow.login import login_manager
from PhoenixNow.model import db
from flask import Flask
import os

def create_app(config_object, register_blueprint=True):
    """
    Sets up a Flask app variable based on a config object -- see config.py. We
    do this so that we can use `flask run` and integrate into things like uwsgi
    better and testing. 
    """

    app = Flask(__name__)
    app.config.from_object(config_object)
    if register_blueprint:
        from PhoenixNow.regular import regular
        from PhoenixNow.admin import admin
        from PhoenixNow.backend import backend
        app.register_blueprint(regular)
        app.register_blueprint(backend, url_prefix='/api')
        app.register_blueprint(admin, url_prefix='/admin')
    
    return app

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).
    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app