import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru/bot/v1"

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


def get_events():

    url = f"{API}/events/get"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:

        r = requests.post(url, headers=headers)

        print("EVENT STATUS:", r.status_code)
        print("EVENT RESPONSE:", r.text)

        if r.status_code == 200:

            data = r.json()

            return data.get("events", [])

    except Exception as e:

        print("EVENT ERROR:", e)

    return []


print("MAX BOT STARTED")

while True:

    events = get_events()

    for ev in events:

        try:

            message = ev.get("message")

            if not message:
                continue

            chat_id = message["chat"]["chat_id"]
            text = message.get("text", "")

            print("MESSAGE:", text)

            send_message(chat_id, "Сообщение получено.")

        except Exception as e:

            print("PROCESS ERROR:", e)

    time.sleep(2)