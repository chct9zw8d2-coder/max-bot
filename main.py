import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://platform-api.max.ru"

headers = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "MAX BOT ONLINE"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    try:
        if data["update_type"] == "message":

            chat_id = data["message"]["chat_id"]
            text = data["message"]["text"].lower()

            if text == "привет":
                send_message(chat_id, "Привет 👋")
            else:
                send_message(chat_id, "Напишите 'привет'")

    except Exception as e:
        print("ERROR:", e)

    return jsonify({"status": "ok"})


def send_message(chat_id, text):

    url = f"{API_URL}/messages"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(url, headers=headers, json=payload)

    print("SEND:", r.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
