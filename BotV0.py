import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, render_template,session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.secret_key = "Hello bots"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='./status.log', level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)
client = Client(os.getenv('USER_SID'), os.getenv('AUTH_KEY'))

data = {
    "tag": "menu",
    "options": ["Start", "Account", "Quit"],

}


@app.route('/')
def init():
    return "we are live!"


@app.route('/messages', methods=['POST'])
def send_message():
    """receives and replies customers requests"""

    logger.info(f"{request.form.get('From')} sent: {request.form.get('Body')} ")

    req = request.form.get('Body')
    if str(req).lower() != 'services':
        return '', 204

    menus = ''
    session["tag"] = data['tag']
    for i, b in enumerate(data['options'], 1):
        menus += f"{str(i)}. {b}\n"

    res = MessagingResponse()
    res.message(f"Here is the menu:\n{menus}")

    n = menus.replace('\n', ' ').rstrip()
    logger.info(f"replying with:  {n} to: {request.form.get('From')} ")

    return str(res)


@app.route('/status', methods=['POST'])
def message_status():
    msg_sid = request.values.get('MessageSid')
    msg_status = request.values.get('MessageStatus')
    receiver = request.values.get('To')
    logger.info(f"Message_SID: {msg_sid} to: {receiver} has Status: {msg_status}")
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
