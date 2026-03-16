import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://platform-api.max.ru/bot/v1"


# -----------------------------
# отправка сообщения
# -----------------------------
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

        r = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        print("SEND STATUS:", r.status_code)
        print("SEND RESPONSE:", r.text)

    except Exception as e:

        print("SEND ERROR:", e)


# -----------------------------
# получение событий (long polling)
# -----------------------------
def get_events():

    url = f"{API}/events"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "limit": 10,
        "timeout": 30
    }

    try:

        r = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=35
        )

        print("EVENT STATUS:", r.status_code)
        print("EVENT RESPONSE:", r.text)

        if r.status_code == 200:

            data = r.json()

            return data.get("events", [])

    except Exception as e:

        print("EVENT ERROR:", e)

    return []


# -----------------------------
# основной цикл
# -----------------------------
def main():

    print("MAX BOT STARTED")

    while True:

        events = get_events()

        print("EVENTS PARSED:", events)

        for ev in events:

            try:

                message = ev.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["chat_id"]

                text = message.get("text", "")

                print("NEW MESSAGE:", text)

                if text == "/start":

                    send_message(
                        chat_id,
                        "👋 Добро пожаловать в стоматологию Райтер!\n\n"
                        "Напишите ваш вопрос или заявку."
                    )

                else:

                    send_message(
                        chat_id,
                        "Спасибо! Администратор скоро ответит."
                    )

            except Exception as e:

                print("PROCESS ERROR:", e)

        time.sleep(1)


# -----------------------------
# запуск
# -----------------------------
if __name__ == "__main__":
    main()
