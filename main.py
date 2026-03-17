import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== НАСТРОЙКИ =====
MAX_TOKEN = os.getenv("MAX_TOKEN")

API_URL = "https://platform-api.max.ru"

HEADERS = {
    "Authorization": f"Bearer {MAX_TOKEN}",  # ✅ ВАЖНО!
    "Content-Type": "application/json"
}


# ===== ПРОВЕРКА СЕРВЕРА =====
@app.route("/")
def home():
    return "MAX BOT WORKING"


# ===== WEBHOOK =====
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("EVENT:", data)

    try:
        if data.get("update_type") == "message_created":

            message = data.get("message", {})

            chat_id = message.get("recipient", {}).get("chat_id")
            text = message.get("body", {}).get("text", "")

            print("CHAT_ID:", chat_id)
            print("TEXT:", text)

            if chat_id and text:
                send_message(chat_id, f"Вы написали: {text}")

    except Exception as e:
        print("ERROR:", e)

    return jsonify({"ok": True})


# ===== ОТПРАВКА СООБЩЕНИЯ =====
def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    response = requests.post(
        f"{API_URL}/messages",
        headers=HEADERS,
        json=payload
    )

    print("SEND STATUS:", response.status_code)
    print("SEND RESPONSE:", response.text)


# ===== ЗАПУСК =====
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
