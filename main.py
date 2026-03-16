import requests
import time
import os

# ====== НАСТРОЙКИ ======

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://platform-api.max.ru/bot/v1"

# ====== КНОПКИ ======

def main_keyboard():
    return {
        "keyboard": [
            [{"text": "🦷 Записаться на прием"}],
            [{"text": "❓ Задать вопрос"}],
            [{"text": "📍 Адрес клиники"}],
            [{"text": "📞 Телефон"}]
        ],
        "resize_keyboard": True
    }

# ====== ОТПРАВКА СООБЩЕНИЯ ======

def send_message(chat_id, text, keyboard=None):

    url = f"{API_URL}/messages/send"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        payload["reply_markup"] = keyboard

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except:
        pass


# ====== ОБРАБОТКА СООБЩЕНИЙ ======

def handle_message(msg):

    chat_id = msg["chat"]["chat_id"]
    text = msg.get("text", "")

    if text == "/start":

        send_message(
            chat_id,
            "👋 Добро пожаловать в стоматологию *Райтер*\n\n"
            "Выберите действие:",
            main_keyboard()
        )

    elif "Записаться" in text:

        send_message(
            chat_id,
            "🦷 Для записи напишите:\n\n"
            "1️⃣ Ваше имя\n"
            "2️⃣ Телефон\n"
            "3️⃣ Удобную дату"
        )

    elif "вопрос" in text.lower():

        send_message(
            chat_id,
            "❓ Напишите ваш вопрос.\n"
            "Администратор ответит вам в ближайшее время."
        )

    elif "Адрес" in text:

        send_message(
            chat_id,
            "📍 Москва\n\n"
            "ул. Примерная 10\n\n"
            "Мы на карте:\n"
            "https://yandex.ru/maps"
        )

    elif "Телефон" in text:

        send_message(
            chat_id,
            "📞 +7 (999) 123-45-67"
        )

    else:

        send_message(
            chat_id,
            "Пожалуйста выберите кнопку 👇",
            main_keyboard()
        )


# ====== ПОЛУЧЕНИЕ ОБНОВЛЕНИЙ ======

def get_updates(offset=None):

    url = f"{API_URL}/updates"

    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    params = {}

    if offset:
        params["offset"] = offset

    try:

        r = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return []


# ====== ОСНОВНОЙ ЦИКЛ ======

def main():

    print("MAX BOT STARTED")

    offset = None

    while True:

        updates = get_updates(offset)

        for upd in updates:

            try:

                message = upd.get("message")

                if message:
                    handle_message(message)

                offset = upd.get("update_id", 0) + 1

            except Exception as e:
                print("ERROR:", e)

        time.sleep(1)


# ====== ЗАПУСК ======

if __name__ == "__main__":
    main()