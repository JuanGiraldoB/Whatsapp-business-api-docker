from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from messages.message_helper import (
    get_text_message_input,
    send_message,
    exists_message,
    is_valid_message,
    get_message
)
from sheets.sheets_helper import add_expense, get_total_expenses
import json

# Create a Blueprint object
routes_bp = Blueprint('routes', __name__)


@routes_bp.route("/webhook/", methods=["POST", "GET"])
async def webhook_whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == current_app.config["VERIFY_TOKEN"]:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    data = request.json

    if not exists_message(data):
        current_app.logger.info("exists message, not sent")
        return "Message does not exists."

    msg = get_message(data)

    if not is_valid_message(msg):
        current_app.logger.info("is valid message, not valid: %s", msg)
        return "Invalid message."

    if 'agregar' in msg:
        message_parts = msg.split(" ")
        amount, msg = message_parts
        current_app.logger.info("Adding expense: %s", msg)
        add_expense(int(amount))

    message = get_text_message_input(
        current_app.config['RECIPIENT_WAID'], msg)

    if 'Ver gastos' in msg:
        total_expenses = get_total_expenses()
        message_dict = json.loads(message)
        message_dict['text']['body'] = f'Gastos totales: {total_expenses}'
        message = json.dumps(message_dict)

    await send_message(message)

    current_app.logger.info("msg was sent: %s", message)

    return jsonify({'status': 'success'}), 200
