from app import webhook_app

from flask import request, abort

@webhook_app.route('/')
def index():
    return '<h1>Home</h1>'
