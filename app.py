from flask import Flask, request
import re

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return "Chatbot de salón de belleza activo"


# 🔽 AGREGAR AQUÍ (debajo de la ruta principal)
@app.route("/mensaje")
def prueba():
    texto = request.args.get("msg", "").lower()
    return procesar_mensaje(texto)


# Lógica del chatbot
def procesar_mensaje(msg):

    if re.search(r"\b(hola|buenas|hey|salon)\b", msg):
        return "Hola 👋 Bienvenido a nuestro salón de belleza. ¿En qué podemos ayudarte?"

    elif re.search(r"\b(servicios|que ofrecen|tratamientos)\b", msg):
        return ("Ofrecemos:\n"
                "💇‍♀️ Corte de cabello\n"
                "💅 Manicure y pedicure\n"
                "🎨 Tinte\n"
                "💆‍♀️ Tratamientos capilares")

    elif re.search(r"\b(precio|costo|cuanto)\b", msg):
        return ("Nuestros precios son:\n"
                "Corte: Q30\n"
                "Manicure: Q40\n"
                "Tinte: desde Q80")

    elif re.search(r"\b(horario|abren|atienden)\b", msg):
        return "Atendemos de lunes a sábado de 8:00 AM a 6:00 PM"

    elif re.search(r"\b(cita|reservar|agendar)\b", msg):
        return "Para agendar una cita, escribe: Quiero cita + servicio + hora"

    elif re.search(r"\b(gracias|ok|adios)\b", msg):
        return "Gracias por contactarnos 💖 ¡Te esperamos!"

    else:
        return "No entendí tu mensaje. Escribe 'servicios' para ver opciones."


if __name__ == "__main__":
    app.run(port=5000)
    