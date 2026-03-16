import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_URL = "https://platform-api.max.ru/bot/v1"


def send_message(chat_id, text):

    url = f"{BASE_URL}/messages/send"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        print("SEND:", r.status_code)
    except Exception as e:
        print("SEND ERROR:", e)


def get_updates():

    url = f"{BASE_URL}/updates"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:
        r = requests.get(url, headers=headers, timeout=30)

        print("UPDATES STATUS:", r.status_code)

        if r.status_code == 200:
            data = r.json()
            print("UPDATES:", data)
            return data

    except Exception as e:
        print("UPDATE ERROR:", e)

    return []


def main():

    print("MAX BOT STARTED")

    while True:

        updates = get_updates()

        if not updates:
            time.sleep(2)
            continue

        for upd in updates:

            try:

                body = upd.get("body", {})
                message = body.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["chat_id"]
                text = message.get("text", "")

                print("MESSAGE:", text)

                if text == "/start":

                    send_message(
                        chat_id,
                        "👋 Добро пожаловать в стоматологию Райтер\n\nНапишите любой вопрос."
                    )

                else:

                    send_message(
                        chat_id,
                        "Спасибо! Администратор ответит вам."
                    )

            except Exception as e:
                print("PROCESS ERROR:", e)

        time.sleep(1)


if __name__ == "__main__":
    main()