import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

HEADERS = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

AARON_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

offset = None

# список клиентов
clients = {}


def get_updates():

    global offset

    params = {
        "timeout": 60
    }

    if offset:
        params["offset"] = offset

    try:

        r = requests.get(
            f"{API}/updates",
            headers=HEADERS,
            params=params,
            timeout=65
        )

        print("STATUS:", r.status_code)

        if r.status_code == 429:
            print("RATE LIMIT — WAIT 60 SEC")
            time.sleep(60)
            return []

        if r.status_code != 200:
            print("ERROR:", r.text)
            time.sleep(10)
            return []

        data = r.json()

        updates = data.get("updates", [])

        if updates:
            offset = updates[-1]["update_id"] + 1

        return updates

    except Exception as e:

        print("CONNECTION ERROR:", e)
        time.sleep(10)
        return []


def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:

        r = requests.post(
            f"{API}/messages/send",
            headers=HEADERS,
            json=payload
        )

        print("SEND:", r.status_code)

    except Exception as e:

        print("SEND ERROR:", e)


print("MAX OPERATOR BOT STARTED")

while True:

    updates = get_updates()

    for u in updates:

        message = u.get("message")

        if not message:
            continue

        text = message.get("text", "")
        chat_id = message["chat"]["chat_id"]

        print("MESSAGE:", chat_id, text)

        # клиент пишет
        if chat_id != AARON_ID:

            clients[chat_id] = True

            forward = f"""
Клиент: {chat_id}

{text}
"""

            send_message(AARON_ID, forward)

            send_message(chat_id, "Сообщение передано оператору.")

        # отвечает Аарон
        else:

            if ":" not in text:
                continue

            client_id, reply = text.split(":", 1)

            client_id = client_id.strip()
            reply = reply.strip()

            send_message(client_id, reply)

    time.sleep(1)
