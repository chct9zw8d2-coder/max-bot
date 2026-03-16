import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TOKEN = os.getenv("MAX_TOKEN")

API_URL = "https://platform-api.max.ru"

headers = {
    "Authorization": MAX_TOKEN,
    "Content-Type": "application/json"
}


@app.route("/")
def home():
    return "MAX BOT WORKING"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    try:

        if data.get("update_type") == "message_created":

            message = data.get("message", {})

            chat_id = message.get("recipient", {}).get("chat_id")

            text = message.get("body", {}).get("text", "")

            if text:

                reply = f"Вы написали: {text}"

                send_message(chat_id, reply)

    except Exception as e:
        print("ERROR:", e)

    return jsonify({"status": "ok"})


def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(
        f"{API_URL}/messages",
        headers=headers,
        json=payload
    )

    print("SEND:", r.text)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
