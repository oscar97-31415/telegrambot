from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
recordatorios = {}

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.startswith("/recordar"):
            try:
                hora, mensaje = text.split(" ", 2)[1:]
                recordatorios[chat_id] = (hora, mensaje)
                enviar_mensaje(chat_id, f"👌 Recordaré '{mensaje}' a las {hora}")
            except:
                enviar_mensaje(chat_id, "❌ Usa el formato: /recordar 20:00 estudiar")
        elif text == "/ver":
            if chat_id in recordatorios:
                enviar_mensaje(chat_id, f"Tens pendent: {recordatorios[chat_id][1]} a les {recordatorios[chat_id][0]}")
            else:
                enviar_mensaje(chat_id, "No tens recordatoris guardats.")

    return "OK", 200

def enviar_mensaje(chat_id, text):
    requests.post(f"{APP_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route("/")
def index():
    return "Bot actiu!"

if __name__ == "__main__":
    app.run(debug=True)
