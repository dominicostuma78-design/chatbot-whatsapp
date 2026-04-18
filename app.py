from flask import Flask, request
import requests
import re

app = Flask(__name__)

# CONFIGURACIÓN
VERIFY_TOKEN = "123456"
ACCESS_TOKEN = "EAAX0sznTwr0BRBFLPl8uRhQij0egZAttnXJUeAzCbF1VfmuCBsLn0gZB6vRLhi7gAFo3N3QZAqG9ULDSRDVskPomQiZCoh5SBfWnFqoMo6NOVGGwpP3GJw8IHQ0F0kZBhOp3jR2Skno377c8oodKxhV7kpPvFkC573NlQlf1bDyDWfCDCcxtcDcYO7mkemad6dAsZBW6mfrVlfGFUNqZCPamVSWDsEPZAhGbKMDv9oUiUbNvMqkcGTy6ErJN696maIZCV1SwoRlZCI0xLzIokXL8BaBdb6"
PHONE_NUMBER_ID = "1100661589791810"

# VERIFICACIÓN WEBHOOK (META)
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Error", 403

# RECIBIR MENSAJES DE WHATSAPP
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = message["text"]["body"].lower()
        sender = message["from"]

        respuesta = procesar_mensaje(text)
        enviar_mensaje(sender, respuesta)

    except Exception as e:
        print("Error al procesar mensaje:", e)

    return "ok", 200

# LÓGICA DEL CHATBOT
def procesar_mensaje(msg):
    msg = msg.lower().strip()

    # SALUDO
    if re.search(r"\b(hola|buenas|hey|salon|informacion)\b", msg):
        return (
            "💇‍♀️ ¡Bienvenido a nuestro Salón de Belleza!\n\n"
            "✨ Puedes consultar:\n"
            "📍 Ubicaciones\n"
            "🕒 Horarios\n"
            "💰 Precios\n"
            "📅 Citas\n"
            "✨ Servicios\n"
            "📦 Disponibilidad\n\n"
            "Escribe lo que necesitas 😊"
        )

    # UBICACIONES
    elif re.search(r"\b(ubicacion|ubicaciones|donde estan|direccion)\b", msg):
        return (
            "📍 Nuestras ubicaciones disponibles:\n"
            "1. Centro de la ciudad\n"
            "2. Zona comercial\n\n"
            "Puedes escribir 'mapa' para más detalles."
        )

    # MAPA
    elif re.search(r"\b(mapa|ubicacion exacta)\b", msg):
        return (
            "📍 Ubicación de referencia:\n"
            "https://maps.google.com\n\n"
            "Te esperamos 💇‍♀️"
        )

    # HORARIOS
    elif re.search(r"\b(horario|horarios|hora|abren|atienden)\b", msg):
        return (
            "🕒 Horario de atención:\n"
            "Lunes a sábado\n"
            "⏰ 8:00 AM - 6:00 PM"
        )

    # PRECIOS Y DISPONIBILIDAD
    elif re.search(r"\b(precio|precios|costo|cuanto|valor|disponible|disponibilidad|tienen|hay espacio)\b", msg):
        return (
            "💰 Información de precios y disponibilidad:\n"
            "💇‍♀️ Corte: Q30\n"
            "💅 Manicure: Q40\n"
            "🎨 Tinte: desde Q80\n"
            "💆‍♀️ Tratamientos: desde Q60\n\n"
            "📅 Actualmente contamos con espacios disponibles.\n"
            "Si deseas reservar, escribe:\n"
            "👉 cita + servicio + hora"
        )

    # SERVICIOS
    elif re.search(r"\b(servicios|que ofrecen|tratamientos)\b", msg):
        return (
            "✨ Servicios disponibles:\n"
            "1. Corte de cabello\n"
            "2. Manicure y pedicure\n"
            "3. Tinte\n"
            "4. Tratamientos capilares"
        )

    # CONFIRMACIÓN DE CITA
    elif re.search(r"^cita\s+[a-záéíóúñ]+\s+\d{1,2}(am|pm)?$", msg):
        return (
            "✅ Tu solicitud de cita fue recibida.\n"
            "📲 En breve confirmaremos disponibilidad.\n"
            "Gracias por confiar en nosotros 💖"
        )

    # CITAS GENERAL
    elif re.search(r"\b(cita|reservar|agendar)\b", msg):
        return (
            "📅 Para agendar una cita escribe:\n"
            "👉 cita + servicio + hora\n\n"
            "Ejemplo:\n"
            "cita manicure 10am"
        )

    # DESPEDIDA
    elif re.search(r"\b(gracias|ok|adios|bye)\b", msg):
        return "💖 Gracias por escribir. ¡Te esperamos en el salón!"

    # MENSAJE NO ENTENDIDO
    else:
        return (
            "🤖 No entendí tu mensaje.\n\n"
            "Puedes escribir:\n"
            "📍 ubicaciones\n"
            "🕒 horarios\n"
            "💰 precios\n"
            "📅 cita\n"
            "✨ servicios"
        )

# ENVIAR MENSAJE A WHATSAPP
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

    response = requests.post(url, headers=headers, json=data)
    print("Respuesta de Meta:", response.status_code, response.text)

# RUTA PRINCIPAL
@app.route("/")
def inicio():
    return "Chatbot activo"

# EJECUCIÓN
if __name__ == "__main__":
    app.run()