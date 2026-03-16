from flask import Flask, request
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru/v1/bot"

app = Flask(__name__)


def send_message(chat_id, text):

    url = f"{API}/messages/send"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, headers=headers, json=payload)


@app.route("/", methods=["POST"])
def webhook():

    data = request.json

    print("EVENT:", data)

    message = data.get("message")

    if not message:
        return "ok"

    chat_id = message["chat"]["chat_id"]
    text = message.get("text", "")

    if text == "/start":

        send_message(
            chat_id,
            "👋 Добро пожаловать в стоматологию Райтер!\n\n"
            "Напишите ваш вопрос или заявку на запись."
        )

    else:

        send_message(
            chat_id,
            "Спасибо! Администратор скоро ответит."
        )

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)