import aiohttp
import json
from flask import current_app


def is_message_valid(data: dict):
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


def get_text_message_input(recipient, text):
    # return json.dumps({
    #     "messaging_product": "whatsapp",
    #     "preview_url": False,
    #     "recipient_type": "individual",
    #     "to": recipient,
    #     "type": "text",
    #     "text": {
    #         "body": text
    #     }
    # })

    return json.dumps(


        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Amorcito"
                },
                "body": {
                    "text": "Te amo muchote"
                },
                "footer": {
                    "text": "Tu solecito"
                },
                "action": {
                    "button": "No funcino :(",
                    "sections": [
                        {
                            "title": "Me amas?",
                            "rows": [
                                {
                                    "id": "SECTION_1_ROW_1_ID",
                                    "title": "No",
                                    "description": "Toy tiste :("
                                },
                                {
                                    "id": "SECTION_1_ROW_2_ID",
                                    "title": "Shi",
                                    "description": "Toy feliz :)"
                                }
                            ]
                        },
                        # {
                        #     "title": "SECTION_2_TITLE",
                        #     "rows": [
                        #         {
                        #             "id": "SECTION_2_ROW_1_ID",
                        #             "title": "SECTION_2_ROW_1_TITLE",
                        #             "description": "SECTION_2_ROW_1_DESCRIPTION"
                        #         },
                        #         {
                        #             "id": "SECTION_2_ROW_2_ID",
                        #             "title": "SECTION_2_ROW_2_TITLE",
                        #             "description": "SECTION_2_ROW_2_DESCRIPTION"
                        #         }
                        #     ]
                        # }
                    ]
                }
            }
        }
    )
