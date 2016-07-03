from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    """ Example endpoint

    Returns "hello"
    """
    return "hello"
