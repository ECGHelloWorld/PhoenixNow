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

def check_token(res):
    if 'token' in res:
        try:
            token = res['token']
            token = token.split()
            decoded_token = jwt.decode(token[1], 'habberdashery212', algorithm='HS512', verify=False)
            res['user'] = User.query.get(decoded_token['user'])
            return res

        except jwt.exceptions.DecodeError:
            raise InvalidUsage("Your token was invalid", status_code=400)
    else:
        raise InvalidUsage("You didn't input all the required information", status_code=400)

def check_input(res, *args):
    if all (k in res for k in args):
        return res
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
    res = check_input(request.get_json(silent=True), 'firstname', 'lastname', 'grade', 'email', 'password')
    user = User.query.filter_by(email=res['email']).first()
    if user is None:
        newuser = create_user(res['firstname'], res['lastname'], res['grade'], res['email'], res['password'])
        return jsonify(generate_token({"result": "success", "action": "register", "user": newuser.id}))
    else:
        raise InvalidUsage("This user has already been created", status_code=400)

@backend.route('/login', methods=['POST'])
def login():
    res = check_input(request.get_json(silent=True), 'email', 'password')
    user = User.query.filter_by(email=res['email'].lower()).first()
    if user is None:
        raise InvalidUsage("This user has not been created", status_code=400)
    else:
        if user.check_password(res['password']):
            return jsonify(generate_token({"result": "success", "action": "login", "user": newuser.id}))

@backend.route('/checkin', methods=['POST'])
def checkin():
    res = check_token(check_input(request.get_json(silent=True), 'lat', 'lon'))

    if lon >= -79.8921061:
        if lon <= -79.8833942:
            if lat <= 36.0984408:
                if lat >= 36.0903956:
                    user = res['user']
                    if user.checkedin:
                        raise InvalidUsage("You have already been checked in", status_code=400)
                    if user is None:
                        raise InvalidUsage("This user does not exist", status_code=400)
                    if user.verified == False:
                        raise InvalidUsage("This user is not verified", status_code=400)
                    else:
                        checkin_user(user)
                        return jsonify({"result": "success", "action": "checkin", token: res['token']})

    raise InvalidUsage("The user is not at Guilford")

@backend.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        res = check_token(check_input(request.get_json(silent=True), 'monday', 'tuesday', 'thursday', 'friday', 'saturday', 'sunday'))
        user = res['user']
        user.monday = res['monday']
        user.tuesday = res['tuesday']
        user.wednesday = res['wednesday']
        user.thursday = res['thursday']
        user.friday = res['friday']
        db.session.commit()
        return jsonify({
            "action": "update schedule",
            "result": "success",
            'monday': user.monday,
            'tuesday': user.tuesday, 
            'wednesday': user.wednesday, 
            'thursday': user.thursday, 
            'friday': user.friday 
            'verified': user.schedule_verified
        }
    elif request.method == "GET":
        res = check_token(check_input(request.get_json(silent=True)))
        user = res['user']
        return jsonify({
            "action": "get schedule",
            "result": "success",
            'monday': user.monday,
            'tuesday': user.tuesday, 
            'wednesday': user.wednesday, 
            'thursday': user.thursday, 
            'friday': user.friday 
            'verified': user.schedule_verified
        }

        
