import aiohttp
import json
from flask import current_app
from messages.response_map import RESPONSE_MAP


def exists_message(data: dict):
    if 'object' not in data:
        return False

    if 'entry' not in data:
        return False

    if not data['entry'][0].get('changes'):
        return False

    if not data['entry'][0]['changes'][0].get('value'):
        return False

    if not data['entry'][0]['changes'][0]['value'].get('messages'):
        return False

    if not data['entry'][0]['changes'][0]['value']['messages'][0]:
        return False

    return True


def get_message(data):
    msg_type = get_message_type(data)

    if msg_type == "interactive":
        return data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['title']

    return data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']


def get_message_type(data):
    if 'interactive' in data['entry'][0]['changes'][0]['value']['messages'][0]:
        return "interactive"

    return "text"


def is_valid_message(msg):
    valid_msgs = ["Gastos", "Agregar gasto", "Ver gastos"]
    return msg in valid_msgs or "agregar" in msg


async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    async with aiohttp.ClientSession() as session:
        url = 'https://graph.facebook.com' + \
            f"/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))


def get_text_message_input(recipient, msg):
    response_data = RESPONSE_MAP.get(msg, RESPONSE_MAP['default'])
    response_data.update({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient
    })

    current_app.logger.info("response data%s", response_data)
    current_app.logger.info("text %s", response_data['text'])
    current_app.logger.info("type %s", response_data['type'])

    # return json.dumps({
    #         "messaging_product": "whatsapp",
    #         "preview_url": False,
    #         "recipient_type": "individual",
    #         "to": recipient,
    #         "type": "text",
    #         "text": {
    #             "body": "Agregado correctamente."
    #         }
    #     })

    return json.dumps({
        'type': response_data['type'],
        'text': response_data['text']
    })
