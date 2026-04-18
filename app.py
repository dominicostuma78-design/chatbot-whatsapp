from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# 🔐 CONFIGURACIÓN
VERIFY_TOKEN = "123456"
ACCESS_TOKEN = "EAAX0sznTwr0BRJZAlZAT2vJPJe5n1SliWCf6svop4BlXKSN5dAcNabZAJklqy82A0IDMogMVHn6da3hZA5BAR53ULNYIL9IORqHl7twkk6W9JophzhKuzBftye0EQdQorkPolvC9mrqXY2kli1aAO199kMZAW5acW16c0vkZCdhCrxl3RN0nv6Wz69ZBDohZA2vbW6O99mZAkZCRbUxgSNcNwctGjZC31ZBfF7egHynTv5bp4w0KyOUysZCm2ICboQLutxXMzz3EEN8engJtgdUbLc4JIqabt"
PHONE_NUMBER_ID = "1100661589791810"

# 🌐 VERIFICACIÓN WEBHOOK (META)
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Error", 403

# 📩 RECIBIR MENSAJES DE WHATSAPP
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = message["text"]["body"].lower()
        sender = message["from"]

        respuesta = procesar_mensaje(text)
        enviar_mensaje(sender, respuesta)

    except:
        pass

    return "ok", 200

# 🧠 LÓGICA DEL CHATBOT
def procesar_mensaje(msg):

    if re.search(r"\b(hola|buenas|hey|salon)\b", msg):
        return "💇‍♀️ Hola, bienvenido al salón de belleza. ¿En qué podemos ayudarte?"

    elif re.search(r"\b(servicios|que ofrecen|tratamientos)\b", msg):
        return ("Ofrecemos:\n"
                "💇‍♀️ Corte de cabello\n"
                "💅 Manicure y pedicure\n"
                "🎨 Tinte\n"
                "💆‍♀️ Tratamientos capilares")

    elif re.search(r"\b(precio|costo|cuanto)\b", msg):
        return ("Precios:\n"
                "Corte: Q30\n"
                "Manicure: Q40\n"
                "Tinte: desde Q80")

    elif re.search(r"\b(horario|abren|atienden)\b", msg):
        return "Horario: lunes a sábado de 8:00 AM a 6:00 PM"

    elif re.search(r"\b(cita|reservar|agendar)\b", msg):
        return "Para agendar cita escribe: cita + servicio + hora"

    elif re.search(r"\b(gracias|ok|adios)\b", msg):
        return "Gracias por escribir 💖"

    else:
        return "No entendí. Escribe 'servicios' para ver opciones."

# 📤 ENVIAR MENSAJE A WHATSAPP
def enviar_mensaje(numero, mensaje):

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensaje
        }
    }

    requests.post(url, headers=headers, json=data)

# 🟢 RUTA PRINCIPAL
@app.route("/")
def inicio():
    return "Chatbot activo"

# 🚀 EJECUCIÓN
if __name__ == "__main__":
    app.run()
