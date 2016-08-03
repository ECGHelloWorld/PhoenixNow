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

    app.secret_key = 'idontknowwhatthisis'

    ### Configuration for flask-mail | "SMPT" Settings | This is the email account that sends emails ###
    app.config["MAIL_SERVER"] = "mail.privateemail.com" # specifies email domain. "smtp.gmail.com" for a gmail account
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'support@chadali.me' # your email address
    app.config["MAIL_PASSWORD"] = 'ask ali for password to his email' # email password
    ### Configuration for flask-mail | If you're using your own email, in views.py change sender='support@chadali.me' to your email ###

    from PhoenixNow.views import mail 
    mail.init_app(app)

    from PhoenixNow.model import db
    db.init_app(app)

    with app.app_context():
        db.create_all()



    
    return app
