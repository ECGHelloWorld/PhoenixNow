import jwt
from flask import Blueprint, jsonify, request
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.user import create_user, checkin_user
from flask_login import login_required, login_user, logout_user
from PhoenixNow.model import User, db

backend = Blueprint('backend', __name__, template_folder='templates', static_folder='static')

def generate_token(result):
    token = jwt.encode(result, 'habberdashery212', algorithm='HS512')
    result['token'] = "Bearer " + token.decode('utf-8')
    return result

def check_input(res, *args):
    if all (k in res for k in args):
        return
    else:
        raise InvalidUsage("You didn't input all the required information", status_code=400)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@backend.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@backend.route('/register', methods=['POST'])
def register():
    res = request.get_json(silent=True)
    check_input(res, 'firstname', 'lastname', 'grade', 'email', 'password')
    user = User.query.filter_by(email=res['email']).first()
    if user is None:
        newuser = create_user(res['firstname'], res['lastname'], res['grade'], res['email'], res['password'])
        return jsonify(generate_token({"result": "success", "action": "register", "user": newuser.id}))
    else:
        raise InvalidUsage("This user has already been created", status_code=400)

@backend.route('/checkin', methods=['POST'])
def checkin():
    res = request.get_json(silent=True)
    check_input(res, 'email')
    user = User.query.filter_by(email=res['email']).first()
    if user is None:
        raise InvalidUsage("This user does not exist", status_code=400)
    if user.verified == False:
        raise InvalidUsage("This user is not verified", status_code=400)
    else:
        checkin_user(user)
        return jsonify(generate_token({"result": "success", "action": "checkin", "email": user.email}))

