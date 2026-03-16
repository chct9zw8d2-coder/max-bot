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

    params = {}

    if offset:
        params["offset"] = offset

    r = requests.get(
        f"{API}/updates",
        headers=HEADERS,
        params=params
    )

    print("STATUS:", r.status_code)
    print("BODY:", r.text)

    if r.status_code != 200:
        time.sleep(30)
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
        headers=HEADERS,
        json=payload
    )

    print("SEND:", r.status_code, r.text)


print("MAX TEST BOT STARTED")

while True:

    updates = get_updates()

    for u in updates:

        message = u.get("message")

        if not message:
            continue

        text = message.get("text", "").lower()
        chat_id = message["chat"]["chat_id"]

        print("MESSAGE:", text)

        if text == "привет":

            send_message(chat_id, "привет")

    time.sleep(40)
