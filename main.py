import os
import requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

HEADERS = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

app = Flask(__name__)


def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(
        f"{API}/messages/send",
        headers=HEADERS,
        json=payload
    )

    print("SEND:", r.status_code, r.text)


@app.route("/")
def home():
    return "MAX BOT ONLINE"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    message = data.get("message")

    if not message:
        return jsonify({"ok": True})

    text = message.get("text", "").lower()
    chat_id = message["chat"]["chat_id"]

    if text == "привет":
        send_message(chat_id, "привет")

    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
