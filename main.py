import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

HEADERS = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

offset = None


def get_updates():

    global offset

    url = f"{API}/updates"

    params = {}

    if offset:
        params["offset"] = offset

    r = requests.get(url, headers=HEADERS, params=params)

    print("STATUS:", r.status_code)

    if r.status_code == 429:

        print("RATE LIMIT — sleeping 20 sec")
        time.sleep(20)
        return []

    if r.status_code != 200:

        print("BODY:", r.text)
        return []

    data = r.json()

    updates = data.get("updates", [])

    if updates:
        offset = updates[-1]["update_id"] + 1

    return updates


def send_message(chat_id, text):

    url = f"{API}/messages/send"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(url, headers=HEADERS, json=payload)

    print("SEND:", r.status_code)


print("MAX BOT STARTED")

while True:

    updates = get_updates()

    for u in updates:

        message = u.get("message")

        if not message:
            continue

        chat_id = message["chat"]["chat_id"]
        text = message.get("text", "")

        print("MESSAGE:", text)

        send_message(chat_id, "Сообщение получено")

    time.sleep(12)
