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

    # SALUDO / INICIO
    if re.search(r"\b(hola|holi|buenas|buenos dias|buenas tardes|buenas noches|hey|informacion|info)\b", msg):
        return (
            "💇‍♀️ ¡Hola! Bienvenido a nuestro Salón de Belleza ELVIA.\n\n"
            "Con gusto puedo ayudarte con:\n"
            "📍 Ubicaciones\n"
            "🕒 Horarios\n"
            "💰 Precios\n"
            "📦 Disponibilidad\n"
            "✨ Servicios\n"
            "📅 Citas\n\n"
            "Escribe la opción que deseas consultar."
        )

    # UBICACIONES
    elif re.search(r"\b(ubicacion|ubicaciones|direccion|direcciones|donde estan|donde se ubican|donde queda|donde quedan|donde se encuentran|sucursales)\b", msg):
        return (
            "📍 Contamos con estas ubicaciones:\n"
            "1. Sucursal Centro de santa cruz del Quiche\n"
            "2. Sucursal Zona 1-calle 4 cuidad de Guatemala\n\n"
            "Si deseas más detalle, escribe: mapa"
        )

    # MAPA
    elif re.search(r"\b(mapa|ubicacion exacta|google maps|maps)\b", msg):
        return (
            "🗺️ Aquí puedes consultar una ubicación de referencia:\n"
            "https://maps.google.com\n\n"
            "Si deseas, también puedo ayudarte con horarios o precios."
        )

    # HORARIOS
    elif re.search(r"\b(horario|horarios|hora|horas|abren|atienden|cuando atienden|que horario atienden|que hora abren)\b", msg):
        return (
            "🕒 Nuestro horario de atención es:\n"
            "Lunes a sábado\n"
            "⏰ 8:00 AM a 6:00 PM\n\n"
            "Si deseas reservar, escribe: cita + servicio + hora"
        )

    # SERVICIOS
    elif re.search(r"\b(servicio|servicios|que ofrecen|que hacen|tratamientos|trabajos|servicios disponibles)\b", msg):
        return (
            "✨ Estos son algunos de nuestros servicios:\n"
            "💇‍♀️ Corte de cabello\n"
            "💅 Manicure y pedicure\n"
            "🎨 Tinte y coloración\n"
            "💆‍♀️ Tratamientos capilares\n\n"
            "También puedes consultar precios o disponibilidad."
        )

    # PRECIOS
    elif re.search(r"\b(precio|precios|costo|costos|cuanto|cuánto|valor|vale|tarifa|tarifas|cuales son sus precios)\b", msg):
        return (
            "💰 Estos son nuestros precios aproximados:\n"
            "💇‍♀️ Corte: Q40\n"
            "💅 Manicure: Q170\n"
            "🎨 Tinte: desde Q300\n"
            "💆‍♀️ Tratamientos: desde Q400\n\n"
            "Si deseas, también puedo indicarte disponibilidad."
        )

    # DISPONIBILIDAD
    elif re.search(r"\b(disponible|disponibilidad|hay espacio|tienen espacio|hay cita|tienen cita|hay cupo|cupo|espacio)\b", msg):
        return (
            "📦 Sí, actualmente contamos con espacios disponibles en agenda.\n\n"
            "Para solicitar una cita escribe así:\n"
            "👉 cita + servicio + hora\n\n"
            "Ejemplo:\n"
            "cita corte 3pm"
        )

    # PRECIO + DISPONIBILIDAD EN UN SOLO MENSAJE
    elif re.search(r"\b(precio|costo|cuanto|valor)\b", msg) and re.search(r"\b(disponible|disponibilidad|espacio|cupo)\b", msg):
        return (
            "💰 En cuanto a precios:\n"
            "💇‍♀️ Corte: Q30\n"
            "💅 Manicure: Q40\n"
            "🎨 Tinte: desde Q80\n"
            "💆‍♀️ Tratamientos: desde Q60\n\n"
            "📦 Además, sí contamos con espacios disponibles.\n"
            "Puedes reservar escribiendo: cita + servicio + hora"
        )

    # CITA ESPECÍFICA
    elif re.search(r"^cita\s+[a-záéíóúñ ]+\s+\d{1,2}(\:\d{2})?\s?(am|pm)?$", msg):
        return (
            "✅ Tu solicitud de cita fue registrada correctamente.\n"
            "📅 En breve confirmaremos la disponibilidad del horario solicitado.\n\n"
            "Gracias por elegir nuestro salón 💖"
        )

    # CITA GENERAL
    elif re.search(r"\b(cita|citas|reservar|reserva|agendar|agendo|quiero una cita|quisiera agendar una cita|quisiera una cita|agendar una cita|quiero una cita)\b", msg):
        return (
            "📅 Para solicitar una cita, escribe el mensaje con este formato:\n"
            "👉 cita + servicio + hora\n\n"
            "Ejemplos:\n"
            "cita corte 3pm\n"
            "cita manicure 10am\n"
            "cita tinte 2pm"
            "asegurese de brindar la informacion correcta de su cita"
        )

    # PRODUCTOS
    elif re.search(r"\b(producto|productos|shampoo|mascarilla|tratamiento capilar|crema)\b", msg):
        return (
            "🧴 También contamos con algunos productos para el cuidado personal.\n"
            "Consulta disponibilidad y precio escribiendo el nombre del producto."
        )

    # AGRADECIMIENTO
    elif re.search(r"\b(gracias|muchas gracias|ok gracias|perfecto gracias)\b", msg):
        return "💖 Con gusto. Estamos para servirte. Si deseas más información, solo escríbenos."

    # DESPEDIDA
    elif re.search(r"\b(adios|adiós|bye|hasta luego|nos vemos)\b", msg):
        return "👋 Gracias por comunicarte con nuestro Salón de Belleza. ¡Será un gusto atenderte!"

    # MENSAJE NO ENTENDIDO
    else:
        return (
            "🤖 No logré entender tu mensaje.\n\n"
            "Puedes escribir, por ejemplo:\n"
            "📍 ubicaciones\n"
            "🕒 horarios\n"
            "💰 precios\n"
            "📦 disponibilidad\n"
            "✨ servicios\n"
            "📅 cita corte 3pm"
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