from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from messages.message_helper import get_text_message_input, send_message, is_message

# Create a Blueprint object
routes_bp = Blueprint('routes', __name__)


@routes_bp.route("/webhook/", methods=["POST", "GET"])
async def webhook_whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == current_app.config["VERIFY_TOKEN"]:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    data = request.json

    if not is_message(data):
        message = get_text_message_input(
            current_app.config['RECIPIENT_WAID'], False)
        await send_message(message)

    message = get_text_message_input(
        current_app.config['RECIPIENT_WAID'], True)
    await send_message(message)

    return jsonify({'status': 'success'}), 200


@routes_bp.route("/")
def index():
    return render_template('index.html', name=__name__)


@routes_bp.route('/welcome', methods=['POST'])
async def welcome():
    data = get_text_message_input(
        current_app.config['RECIPIENT_WAID'], 'Welcome to the Flight Confirmation Demo App for Python!')
    await send_message(data)

    return redirect(url_for('index'))
