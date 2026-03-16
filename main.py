import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

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

    r = requests.post(url, headers=headers, json=payload)

    print("SEND:", r.status_code, r.text)


def get_updates():

    url = f"{API}/updates"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:

        r = requests.get(url, headers=headers)

        print("UPDATES:", r.status_code)
        print("BODY:", r.text)

        if r.status_code == 200:

            data = r.json()

            return data.get("updates", [])

    except Exception as e:

        print("ERROR:", e)

    return []


print("MAX BOT STARTED")

while True:

    updates = get_updates()

    for u in updates:

        try:

            message = u.get("message")

            if not message:
                continue

            chat_id = message["chat"]["chat_id"]
            text = message.get("text", "")

            print("MESSAGE:", text)

            send_message(chat_id, "Сообщение получено")

        except Exception as e:

            print("PROCESS ERROR:", e)

    time.sleep(2)
