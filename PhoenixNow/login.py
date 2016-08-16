from flask_login import LoginManager
from PhoenixNow.model import User

login_manager = LoginManager()
login_manager.login_view = "regular.signin"

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user
