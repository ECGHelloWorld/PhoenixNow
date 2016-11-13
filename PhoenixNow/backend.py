import jwt
from flask import Blueprint, jsonify, request
from PhoenixNow.mail import generate_confirmation_token, confirm_token, send_email
from PhoenixNow.user import create_user, checkin_user, get_weekly_checkins
from flask_login import login_required, login_user, logout_user
from PhoenixNow.model import User, db
from PhoenixNow.code import code
from PhoenixNow.week import Week
import datetime

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

def check_code(res):
    if 'code' in res:
        if res['code'] == code.code:
            return res
        else:
            raise InvalidUsage("Your code was invalid", status_code=400)
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
    res = check_code(check_input(request.get_json(silent=True), 'firstname', 'lastname', 'grade', 'email', 'password'))
    user = User.query.filter_by(email=res['email']).first()
    if user is None:
        newuser = create_user(res['firstname'], res['lastname'], res['grade'], res['email'], res['password'])
        return jsonify(generate_token({"result": "success", "action": "register", "user": newuser.id}))
    else:
        raise InvalidUsage("This user has already been created", status_code=400)

@backend.route('/login', methods=['POST'])
def login():
    res = check_code(check_input(request.get_json(silent=True), 'email', 'password'))
    user = User.query.filter_by(email=res['email'].lower()).first()
    if user is None:
        raise InvalidUsage("This user has not been created", status_code=400)
    else:
        if user.check_password(res['password']):
            return jsonify(generate_token({"result": "success", "action": "login", "user": user.id}))
        else:
            raise InvalidUsage("The password provided was not correct", status_code=400)

@backend.route('/checkin', methods=['POST'])
def checkin():
    #res = check_code(check_token(check_input(request.get_json(silent=True), 'lat', 'lon')))
    res = check_code(check_token(check_input(request.get_json(silent=True))))
 
    if request.remote_addr.rsplit('.',1)[0] in ['192.154.63']:
      user = res['user']
      if user is None:
        raise InvalidUsage("This user does not exist", status_code=400)
      if user.verified == False:
        raise InvalidUsage("This user is not verified", status_code=400)
      else:
        if checkin_user(user):
          return jsonify({"result": "success", "action": "checkin", "token": res['token']})
        else:
          raise InvalidUsage("Already checked in for today")

    else:
      res = check_code(check_token(check_input(request.get_json(silent=True), 'lat', 'lon')))

      lon = float(res['lon'])
      lat = float(res['lat'])

      if lon >= -79.8921061:
          if lon <= -79.8833942:
              if lat <= 36.0984408:
                  if lat >= 36.0903956:
                      user = res['user']
                      #if user.checkedin:
                          #raise InvalidUsage("You have already been checked in", status_code=400)
                      if user is None:
                          raise InvalidUsage("This user does not exist", status_code=400)
                      if user.verified == False:
                          raise InvalidUsage("This user is not verified", status_code=400)
                      else:
                          if checkin_user(user):
                              return jsonify({"result": "success", "action": "checkin", "token": res['token']})
                          else:
                              raise InvalidUsage("Already checked in for today")
      raise InvalidUsage("GPS check failed.")
    raise InvalidUsage("Something is wrong in the backend or request.")

@backend.route('/schedule', methods=['GET', 'POST'])
def schedule():
    res =  check_code(check_token(check_input(request.get_json(silent=True), 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')))
    user = res['user']
    user.schedule = ""
    if res['monday']:
        user.schedule = "M"
        user.schedule_monday = True
    if res['tuesday']:
        user.schedule = "%s:T" % (user.schedule)
        user.schedule_tuesday = True
    if res['wednesday']:
        user.schedule = "%s:W" % (user.schedule)
        user.schedule_wednesday = True
    if res['thursday']:
        user.schedule = "%s:R" % (user.schedule)
        user.schedule_thursday = True
    if res['friday']:
        user.schedule = "%s:F" % (user.schedule)
        user.schedule_friday = True
    if user.schedule == "M:T:W:R:F":
        user.schedule_verified = True
    else:
        user.schedule_verified = False
    db.session.commit()
    return jsonify({
        "action": "update schedule",
        "result": "success",
        'schedule': user.schedule,
        'verified': user.schedule_verified,
        'token': res['token']
    })

@backend.route('/getschedule', methods=['POST'])
def getschedule():
    res = check_code(check_token(check_input(request.get_json(silent=True))))
    user = res['user']
    return jsonify({
        "action": "get schedule",
        "result": "success",
        'schedule': user.schedule,
        'verified': user.schedule_verified,
        'token': res['token']
    })

@backend.route('/getcheckins', methods=['POST'])
def getcheckins():
    res = check_code(check_token(check_input(request.get_json(silent=True))))
    if 'date' in res:
      user = res['user']
      searchdate = datetime.datetime.strptime(res['date'], '%Y-%m-%d').date()
      weekly_checkins = get_weekly_checkins(searchdate)
      week = weekly_checkins.create_week_object(user)
      return jsonify({
          "action": "get checkins",
          "result": "success",
          'monday': week.monday,
          'tuesday': week.tuesday,
          'wednesday': week.wednesday,
          'thursday': week.thursday,
          'friday': week.friday,
          'token': res['token']
      })
    else:
      raise InvalidUsage("No date provided.")
