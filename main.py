import requests
import time
import os

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
API = "https://platform-api.max.ru/bot/v1"  # Базовый API MAX

# Функция для отправки сообщений
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
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# Функция для получения событий
def get_events():
    url = f"{API}/events"
    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        events = response.json().get("events", [])
        return events
    except requests.exceptions.RequestException as e:
        print(f"Error getting events: {e}")
        return []

# Основная функция
def main():
    print("Bot started...")
    
    while True:
        events = get_events()
        
        for event in events:
            message = event.get("message")
            if message:
                chat_id = message["chat"]["id"]
                text = message.get("text", "").lower()

                print(f"Message: {text}")

                if text == "привет":
                    send_message(chat_id, "Привет!")
                else:
                    send_message(chat_id, "Я вас понял! Напишите 'привет' для общения.")
        
        # Задержка перед следующим запросом
        time.sleep(2)

# Запуск
if __name__ == "__main__":
    main()
