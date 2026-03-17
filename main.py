import os
import requests
from flask import Flask, request

app = Flask(__name__)

MAX_TOKEN = os.getenv("MAX_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("EVENT:", data)

    try:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        print("CHAT_ID:", chat_id)
        print("TEXT:", text)

        send_message(chat_id, f"Ты написал: {text}")

    except Exception as e:
        print("ERROR:", e)

    return "ok"

def send_message(chat_id, text):
    url = "https://platform-api.max.ru/bot/send"

    headers = {
        "Authorization": f"Bearer {MAX_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "chat_id": chat_id,
        "message": {
            "text": text
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    print("SEND STATUS:", response.status_code)
    print("SEND RESPONSE:", response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
