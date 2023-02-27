from telebot import TeleBot, types

from ask_me_bot.questions.services import get_question_and_answers
from config import BOT_TOKEN


bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message) -> None:
    """Displays a welcome message and start menu to the user."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Хочу пройти тесты")
    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def send_quiz(message: types.Message) -> None:
    """Sends a quiz at the click of a button"""
    data = get_question_and_answers()
    bot.send_poll(
        message.chat.id,
        question=data[0],
        options=data[1],
        type='quiz',
        correct_option_id=data[2]
    )


if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)
