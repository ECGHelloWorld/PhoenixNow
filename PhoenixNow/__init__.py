from flask import Flask
from PhoenixNow.views import regular

def create_app(config_object):
    """
    Sets up a Flask app variable based on a config object -- see config.py. We
    do this so that we can use `flask run` and integrate into things like uwsgi
    better and testing. 
    """

    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(regular)

    from PhoenixNow.model import db
    db.init_app(app)

    with app.app_context():
        db.create_all()



    
    return app
