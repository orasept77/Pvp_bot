from flask import Flask
from flask_sslify import SSLify

from data.config import DEBUG, SECRET_KEY

webhook_app = Flask(__name__)

if DEBUG is False:
    sslify = SSLify(webhook_app)
    webhook_app.config['FLASK_ENV'] = 'production'
else:
    webhook_app.config['ENV'] = 'development'

webhook_app.config['SECRET_KEY'] = SECRET_KEY
webhook_app.config['TESTING'] = DEBUG
webhook_app.config['DEBUG'] = DEBUG
