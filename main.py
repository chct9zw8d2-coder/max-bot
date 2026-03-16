import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID пользователя Аарон
AARON_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

API = "https://platform-api.max.ru/bot/v1"

# храним соответствие
# сообщение от клиента -> chat_id клиента
clients = {}


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

    try:
        r = requests.post(url, headers=headers, json=payload)
        print("SEND STATUS:", r.status_code)

    except Exception as e:
        print("SEND ERROR:", e)


def get_events():

    url = f"{API}/events"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:

        r = requests.get(url, headers=headers, timeout=30)

        if r.status_code == 200:

            data = r.json()

            return data.get("events", [])

        else:

            print("EVENT STATUS:", r.status_code)

    except Exception as e:

        print("EVENT ERROR:", e)

    return []


def handle_client(chat_id, text):

    print("CLIENT:", chat_id, text)

    clients[chat_id] = chat_id

    message_for_aaron = f"""
Новое сообщение клиента

ID клиента:
{chat_id}

Сообщение:
{text}

Ответь на это сообщение.
"""

    send_message(AARON_ID, message_for_aaron)

    send_message(
        chat_id,
        "Ваше сообщение передано администратору."
    )


def handle_aaron(text):

    print("AARON REPLY:", text)

    if len(clients) == 0:
        return

    # отправляем последнему клиенту
    last_client = list(clients.keys())[-1]

    send_message(last_client, text)


def main():

    print("MAX BOT STARTED")

    while True:

        events = get_events()

        for ev in events:

            try:

                message = ev.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["chat_id"]

                sender = message["sender"]["user_id"]

                text = message.get("text", "")

                print("MESSAGE:", sender, text)

                if sender == AARON_ID:

                    handle_aaron(text)

                else:

                    handle_client(chat_id, text)

            except Exception as e:

                print("PROCESS ERROR:", e)

        time.sleep(2)


if __name__ == "__main__":
    main()