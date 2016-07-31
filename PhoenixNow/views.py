from flask import Blueprint

regular = Blueprint('regular', __name__, template_folder='templates')

@regular.route('/hello')
def hello():
    """
    Example endpoint

    Returns "hello"
    """
    return "hello"
