from telebot import TeleBot, types
import random

from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


def questions_and_answers() -> tuple:
    """We take questions from the database in the form of a dict.
       Then we mix all possible answers and fix the index of the correct answer"""
    questions = {
        "2 + 2": ["4", "2", "6"],
        "Работаешь в гугле?": ["Нет", "Да"],
        "Успел прочитать 'Чистый Python?'": ["Нет", "Вот-вот начну", "Да"]
    }
    random_key = random.choice(list(questions))  # Берем рандомный ключ из dict-а с вопросами.
    answer_for_key = questions[random_key]  # Так же фиксируем варианты ответа от ключа
    index_correct_answer = int()

    answer = questions[random_key][0]  # В БД храним правильный ответ всегда первым.
                                       # Поэтому можем его фиксировать перед перемешиванием

    random.shuffle(answer_for_key)  # Перемешиваем варианты ответа
    for ind, variant in enumerate(answer_for_key):
        if variant == answer:  # Как только наш заранее зафиксированный ответ == перебираемому
            index_correct_answer = ind  # Фиксируем индекс правильного ответа в перемешанном списке.
            break

    return random_key, answer_for_key, index_correct_answer


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
    get_q = questions_and_answers()
    bot.send_poll(message.chat.id,
                  question=get_q[0],
                  options=get_q[1],
                  type='quiz',
                  correct_option_id=get_q[2])


if __name__ == "__main__":
    bot.polling()
