import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru"

ADMIN_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

HEADERS = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

offset = None
clients = {}
last_client = None


def send_message(chat_id, text):

    url = f"{API}/messages/send"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:

        r = requests.post(url, headers=HEADERS, json=payload)

        print("SEND:", r.status_code)

        if r.status_code != 200:
            print("SEND BODY:", r.text)

    except Exception as e:
        print("SEND ERROR:", e)


def get_updates():

    global offset

    url = f"{API}/updates"

    params = {}

    if offset:
        params["offset"] = offset

    try:

        r = requests.get(url, headers=HEADERS, params=params)

        print("UPDATES:", r.status_code)

        if r.status_code == 200:

            data = r.json()

            updates = data.get("updates", [])

            if updates:
                offset = updates[-1]["update_id"] + 1

            return updates

        if r.status_code == 429:
            print("RATE LIMIT")
            time.sleep(10)

        else:
            print("BODY:", r.text)

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
            user_id = message["sender"]["user_id"]
            text = message.get("text", "")

            print("MESSAGE:", user_id, text)

            global last_client

            # если пишет администратор
            if user_id == ADMIN_ID:

                if last_client:
                    send_message(last_client, text)

                else:
                    send_message(chat_id, "Нет активных клиентов.")

            # если пишет клиент
            else:

                clients[chat_id] = chat_id
                last_client = chat_id

                send_message(
                    ADMIN_ID,
                    f"Сообщение клиента:\n{text}"
                )

                send_message(
                    chat_id,
                    "Сообщение отправлено администратору."
                )

        except Exception as e:
            print("PROCESS ERROR:", e)

    # важная задержка для MAX API
    time.sleep(6)
