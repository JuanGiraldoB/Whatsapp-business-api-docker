import json
from flask import Flask, render_template, request, jsonify
import flask
from messages.message_helper import get_text_message_input, send_message
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

config = {
    "APP_ID": os.getenv("APP_ID"),
    "APP_SECRET": os.getenv("APP_SECRET"),
    "RECIPIENT_WAID": os.getenv("RECIPIENT_WAID"),
    "VERSION": os.getenv("VERSION"),
    "PHONE_NUMBER_ID": os.getenv("PHONE_NUMBER_ID"),
    "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
    "VERIFY_TOKEN": os.getenv("VERIFY_TOKEN")
}

app.config.update(config)


@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    """__summary__: Get message from the webhook"""

    if request.method == "GET":
        if request.args.get('hub.verify_token') == config["VERIFY_TOKEN"]:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."

    # RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data = request.get_json()
    # EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    # mensaje = "Telefono:" + \
    #     data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    # mensaje = mensaje+"|Mensaje:" + \
    #     data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    # ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    f = open("texto.txt", "w")
    f.write(data)
    f.close()
    # RETORNAMOS EL STATUS EN UN JSON
    return jsonify({"status": "success"}, 200)


@app.route("/")
def index():
    return render_template('index.html', name=__name__)


@app.route('/welcome', methods=['POST'])
async def welcome():
    data = get_text_message_input(
        app.config['RECIPIENT_WAID'], 'Welcome to the Flight Confirmation Demo App for Python!')
    await send_message(data)
    return flask.redirect(flask.url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
