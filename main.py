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

    except Exception as e:
        print("SEND ERROR:", e)


# -----------------------------
# получение событий
# -----------------------------
def get_events():

    url = f"{API}/events"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print("EVENT STATUS:", r.status_code)

        if r.status_code == 200:

            data = r.json()

            if "events" in data:
                return data["events"]

    except Exception as e:

        print("EVENT ERROR:", e)

    return []


# -----------------------------
# основной цикл
# -----------------------------
def main():

    print("MAX BOT STARTED")

    while True:

        try:

            events = get_events()

            for ev in events:

                message = ev.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["chat_id"]

                text = message.get("text", "")

                print("MESSAGE:", text)

                # команда старт
                if text == "/start":

                    send_message(
                        chat_id,
                        "👋 Добро пожаловать в стоматологию Райтер!\n\n"
                        "Вы можете:\n"
                        "• задать вопрос\n"
                        "• записаться на прием\n"
                        "• узнать стоимость лечения"
                    )

                else:

                    send_message(
                        chat_id,
                        "Спасибо! Администратор скоро ответит."
                    )

        except Exception as e:

            print("PROCESS ERROR:", e)

        time.sleep(2)


# -----------------------------
# запуск
# -----------------------------
if __name__ == "__main__":
    main()