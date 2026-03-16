import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TOKEN = os.getenv("MAX_TOKEN")
API_URL = "https://platform-api.max.ru"

headers = {
    "Authorization": f"Bearer {MAX_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "MAX BOT WORKING"

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    if data.get("update_type") == "message_created":

        message = data.get("message", {})
        chat_id = message.get("recipient", {}).get("chat_id")
        text = message.get("body", {}).get("text", "")

        if chat_id and text:
            send_message(chat_id, f"Вы написали: {text}")

    return jsonify({"ok": True})


def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(
        f"{API_URL}/messages",
        headers=headers,
        json=payload
    )
