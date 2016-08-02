from flask import Blueprint
from flask import Flask, render_template, request, flash, session, redirect, url_for

regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')

@regular.route('/')
def home():
    return render_template('home.html')

@regular.route('/hello')
def hello():
    """
    Example endpoint

    Returns "hello"
    """
    return "hello"


