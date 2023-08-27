RESPONSE_MAP = {
    "Gastos": {
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Desea..."
            },
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {
                        "id": "agregar_gasto", "title": "Agregar gasto"}},
                    {"type": "reply", "reply": {
                        "id": "ver_gastos", "title": "Ver gastos"}}
                ]
            }
        }
    },
    "Agregar gasto": {
        "type": "text",
        "text": {"body": "Para agregar un gasto, digite la cantidad, seguido de la palabra 'agregar', Por ejemplo: xxxxxxx agregar"}
    },
    "agregar": {
        "type": "text",
        "text": {"body": "Agregado correctamente."}
    },
    "Ver gastos": {
        "type": "text",
        "text": {"body": ""}
    },
    "default": {
        "type": "text",
        "text": {"body": "Mensaje invalido"}
    }
}
