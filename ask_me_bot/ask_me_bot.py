from telebot import TeleBot

from config import BOT_TOKEN


bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message) -> None:
    """Displays a welcome message and start menu to the user."""

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:",
        reply_markup=None,
    )


if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)
