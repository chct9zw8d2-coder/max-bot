import os
from maxbot import Bot, Dispatcher, Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администратора (Аарон)
ADMIN_ID = "f9LHodD0cOL-WYXnRJyS7mWEBoC7ycc-eOamlsDOOUxot0lWpbnAKADh3CE"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# запоминаем клиентов
clients = {}


@dp.message()
async def handle_message(message: Message):

    user_id = message.user_id
    chat_id = message.chat_id
    text = message.text

    print("MESSAGE:", user_id, text)

    # если пишет администратор
    if user_id == ADMIN_ID:

        if not clients:
            await bot.send_message(chat_id, "Нет активных клиентов.")
            return

        last_client = list(clients.keys())[-1]

        await bot.send_message(
            last_client,
            text
        )

    # если пишет клиент
    else:

        clients[chat_id] = chat_id

        await bot.send_message(
            ADMIN_ID,
            f"Новое сообщение клиента:\n{text}"
        )

        await bot.send_message(
            chat_id,
            "Сообщение отправлено администратору."
        )


if __name__ == "__main__":

    print("MAX BOT STARTED")

    bot.start_polling(dp)
