
# ================================
# MAX Clinic Bot (Ultra Stable)
# Designed for Railway / VPS / local
# Long polling bot for MAX messenger
# ================================

import time
import requests
import traceback

# ===== НАСТРОЙКИ =====

BOT_TOKEN = "f9LHodD0cOKnaJcfw7a9fQ5Ao6bT1Cmm46D3L97Ntetf8ZBNN1bOMcyMCPrHUK6rvXWVROIdPnEHvme_ViL9"

TARGET_USER_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw4lBGO2bnrPptIYCY7RNSMuGdXkxUzo51Qd9ci8bM5NeDdYkM2tU3DGHihTH9QGuBeXw/exec"

CLINIC_NAME = "Райтер стоматология"
CITY = "Москва"
ADDRESS = "Москва, Саратовская 24"
PHONE = "+7 495 650-23-00"

API_SEND = "https://platform-api.max.ru/messages"
API_UPDATES = "https://platform-api.max.ru/updates"

HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

# ===== СОСТОЯНИЯ =====

last_update = None
user_state = {}
user_data = {}

# ===== УНИВЕРСАЛЬНЫЙ HTTP =====

def safe_post(url, payload):

    try:

        r = requests.post(
            url,
            json=payload,
            headers=HEADERS,
            timeout=15
        )

        return r

    except Exception as e:

        print("POST ERROR:", e)
        return None


# ===== ОТПРАВКА СООБЩЕНИЯ =====

def send_message(chat_id, text):

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    safe_post(API_SEND, payload)


# ===== GOOGLE SHEETS =====

def send_to_google(data):

    payload = {
        "name": data.get("name",""),
        "phone": data.get("phone",""),
        "date": data.get("date",""),
        "question": data.get("question",""),
        "user": data.get("user","")
    }

    try:

        r = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=10
        )

        print("Google response:", r.text)

    except Exception as e:

        print("Google error:", e)


# ===== МЕНЮ =====

def show_menu(chat_id):

    text = (
        "Здравствуйте!\n\n"
        + CLINIC_NAME + "\n"
        + CITY + "\n\n"
        + "Выберите действие:\n"
        + "1 - Записаться на прием\n"
        + "2 - Задать вопрос\n"
        + "3 - Адрес клиники\n"
        + "4 - Позвонить"
    )

    send_message(chat_id, text)

    user_state[chat_id] = "menu"


# ===== ПОЛУЧЕНИЕ СООБЩЕНИЙ =====

def get_updates():

    global last_update

    params = {}

    if last_update:

        params["offset"] = last_update

    try:

        r = requests.get(
            API_UPDATES,
            headers=HEADERS,
            params=params,
            timeout=20
        )

        return r.json()

    except Exception as e:

        print("UPDATE ERROR:", e)

        return {}


# ===== ОБРАБОТКА СООБЩЕНИЙ =====

def process_updates(data):

    global last_update

    if "updates" not in data:
        return

    for upd in data["updates"]:

        last_update = upd["update_id"] + 1

        try:

            msg = upd["message"]
            chat_id = msg["chat"]["chat_id"]
            text = msg.get("text","")

        except:
            continue

        state = user_state.get(chat_id,"menu")

        text_low = text.lower()


        # ===== СТАРТ =====

        if text_low in ["start","старт","/start"]:

            show_menu(chat_id)
            continue


        # ===== ГЛАВНОЕ МЕНЮ =====

        if state == "menu":

            if text == "1":

                send_message(chat_id,"Как вас зовут?")

                user_state[chat_id] = "wait_name"
                user_data[chat_id] = {}

                continue

            if text == "2":

                send_message(chat_id,"Напишите ваш вопрос")

                user_state[chat_id] = "wait_question"

                continue

            if text == "3":

                send_message(chat_id,"Адрес: " + ADDRESS)

                continue

            if text == "4":

                send_message(chat_id,"Телефон: " + PHONE)

                continue


        # ===== ИМЯ =====

        if state == "wait_name":

            user_data[chat_id]["name"] = text

            send_message(chat_id,"Введите телефон")

            user_state[chat_id] = "wait_phone"

            continue


        # ===== ТЕЛЕФОН =====

        if state == "wait_phone":

            phone = text.replace(" ","")

            user_data[chat_id]["phone"] = phone

            send_message(chat_id,"Введите дату и время приема")

            user_state[chat_id] = "wait_date"

            continue


        # ===== ДАТА =====

        if state == "wait_date":

            user_data[chat_id]["date"] = text

            lead = (
                "Новая запись\n\n"
                + "Имя: " + user_data[chat_id]["name"] + "\n"
                + "Телефон: " + user_data[chat_id]["phone"] + "\n"
                + "Дата: " + user_data[chat_id]["date"]
            )

            send_message(TARGET_USER_ID, lead)

            send_to_google({
                "name": user_data[chat_id]["name"],
                "phone": user_data[chat_id]["phone"],
                "date": user_data[chat_id]["date"],
                "user": chat_id
            })

            send_message(chat_id,"Спасибо! Ваша заявка отправлена.")

            show_menu(chat_id)

            continue


        # ===== ВОПРОС =====

        if state == "wait_question":

            send_message(
                TARGET_USER_ID,
                "Вопрос пациента:\n\n" + text
            )

            send_to_google({
                "question": text,
                "user": chat_id
            })

            send_message(
                chat_id,
                "Спасибо! Ваш вопрос передан специалисту."
            )

            show_menu(chat_id)


# ===== ОСНОВНОЙ ЦИКЛ =====

def main():

    print("MAX clinic bot started")

    error_count = 0

    while True:

        try:

            updates = get_updates()

            process_updates(updates)

            error_count = 0

        except Exception as e:

            error_count += 1

            print("CRITICAL ERROR:", e)
            traceback.print_exc()

            # если много ошибок подряд — пауза
            if error_count > 5:

                print("Too many errors. Sleeping 30 sec...")
                time.sleep(30)
                error_count = 0

        time.sleep(2)


if __name__ == "__main__":

    main()
