from app import webhook_app

from flask import request, abort

@webhook_app.route('/webhook', methods=['POST'])
@webhook_app.route('/webhook/', methods=['POST'])
def webhook():
    try:
        data = request.json
    except:
        print('Cant load JSON data')

