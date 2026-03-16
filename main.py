import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

headers = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

offset = None


def get_updates():

    global offset

    params = {}

    if offset:
        params["offset"] = offset

    r = requests.get(
        f"{API}/updates",
        headers=headers,
        params=params
    )

    print("STATUS:", r.status_code)

    if r.status_code == 429:

        print("RATE LIMIT — WAIT 60 sec")
        time.sleep(60)
        return []

    if r.status_code != 200:

        print("ERROR:", r.text)
        time.sleep(60)
        return []

    data = r.json()

    updates = data.get("updates", [])

    if updates:
        offset = updates[-1]["update_id"] + 1

    return updates


def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(
        f"{API}/messages/send",
        headers=headers,
        json=payload
    )

    print("SEND:", r.status_code)


print("MAX BOT STARTED")

while True:

    updates = get_updates()

    for u in updates:

        msg = u.get("message")

        if not msg:
            continue

        chat_id = msg["chat"]["chat_id"]
        text = msg.get("text")

        print("MESSAGE:", text)

        send_message(chat_id, "Сообщение получено")

    time.sleep(45)
