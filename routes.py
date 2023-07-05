from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from messages.message_helper import (
    get_text_message_input,
    send_message,
    exists_message,
    is_valid_message,
    get_message
)
import gspread

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
        # message = get_text_message_input(
        #     current_app.config['RECIPIENT_WAID'], False)
        # await send_message(message)
        current_app.logger.info("exists message, not sent")
        return "Authentication failed. Invalid Token."

    msg = get_message(data)

    if not is_valid_message(msg):
        current_app.logger.info("is valid message, not valid:", msg)
        return "Authentication failed. Invalid Token."

    message = get_text_message_input(
        current_app.config['RECIPIENT_WAID'], msg)
    await send_message(message)

    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("Accounting")

    wks = sh.worksheet("Deudas")

    # print("Rows: ", wks.row_count)
    # print("Cols: ", wks.col_count)

    # print(wks.acell('A2').value)
    # print(wks.get("A1:D5"))

    # print(wks.get_all_records())
    # print(wks.get_all_values())

    wks.update('A22', 'hola')

    current_app.logger.info("msg was sent:", message)

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
