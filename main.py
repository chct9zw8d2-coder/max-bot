import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru/bot/v1"


def send_message(chat_id, text, keyboard=None):

    url = f"{API}/messages/send"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    try:
        requests.post(url, headers=headers, json=data, timeout=10)
    except:
        pass


def keyboard():

    return {
        "keyboard": [
            [{"text": "🦷 Записаться"}],
            [{"text": "❓ Вопрос"}],
            [{"text": "📍 Адрес"}],
            [{"text": "📞 Телефон"}]
        ],
        "resize_keyboard": True
    }


def handle_message(message):

    chat_id = message["chat"]["chat_id"]
    text = message.get("text", "")

    print("MESSAGE:", text)

    if text == "/start":

        send_message(
            chat_id,
            "👋 Добро пожаловать в стоматологию *Райтер*\n\nВыберите действие:",
            keyboard()
        )

    elif "Записаться" in text:

        send_message(
            chat_id,
            "🦷 Напишите:\n\nИмя\nТелефон\nУдобную дату"
        )

    elif "Вопрос" in text:

        send_message(
            chat_id,
            "❓ Напишите ваш вопрос."
        )

    elif "Адрес" in text:

        send_message(
            chat_id,
            "📍 Москва\nул. Примерная 10\n\nhttps://yandex.ru/maps"
        )

    elif "Телефон" in text:

        send_message(
            chat_id,
            "📞 +7 (999) 123-45-67"
        )

    else:

        send_message(
            chat_id,
            "Выберите кнопку 👇",
            keyboard()
        )


def get_updates(offset=None):

    url = f"{API}/updates"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    params = {}

    if offset:
        params["offset"] = offset

    try:

        r = requests.get(url, headers=headers, params=params, timeout=30)

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return []


def main():

    print("MAX BOT STARTED")

    offset = None

    while True:

        updates = get_updates(offset)

        for upd in updates:

            try:

                body = upd.get("body", {})

                message = body.get("message")

                if message:
                    handle_message(message)

                offset = upd.get("update_id", 0) + 1

            except Exception as e:
                print("ERROR:", e)

        time.sleep(1)


if __name__ == "__main__":
    main()