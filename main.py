import os
import requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID пользователя Аарон
AARON_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

API = "https://platform-api.max.ru/bot/v1"

app = Flask(__name__)

# храним клиентов
clients = {}


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

    try:

        r = requests.post(url, headers=headers, json=payload)

        print("SEND STATUS:", r.status_code)
        print("SEND RESPONSE:", r.text)

    except Exception as e:

        print("SEND ERROR:", e)


@app.route("/", methods=["GET"])
def home():
    return "MAX bot running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("EVENT:", data)

    try:

        message = data.get("message")

        if not message:
            return jsonify({"status": "ok"})

        chat_id = message["chat"]["chat_id"]
        sender_id = message["sender"]["user_id"]
        text = message.get("text", "")

        print("MESSAGE:", sender_id, text)

        # если пишет Аарон
        if sender_id == AARON_ID:

            if len(clients) == 0:
                return jsonify({"status": "no client"})

            last_client = list(clients.keys())[-1]

            send_message(last_client, text)

        else:

            clients[chat_id] = chat_id

            send_message(
                AARON_ID,
                f"Сообщение клиента:\n{text}"
            )

            send_message(
                chat_id,
                "Сообщение отправлено администратору."
            )

    except Exception as e:

        print("PROCESS ERROR:", e)

    return jsonify({"status": "ok"})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)