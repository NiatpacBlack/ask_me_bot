import time
from datetime import datetime

from telebot import TeleBot, types

from questions.services import get_question_and_answers
from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)

total_points = 0

correct_user_responses = []
all_user_responses = []


@bot.message_handler(commands=["/"])
def start(message: types.Message) -> None:
    """Displays a welcome message and start menu to the user."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Викторина без времени")
    btn2 = types.KeyboardButton("Блиц")
    markup.add(btn1, btn2)
    msg = bot.send_message(
        message.chat.id,
        text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, blic_or_without_timer)


def blic_or_without_timer(message: types.Message) -> None:
    """Depending on the user's choice, sends him either a quiz with or without time"""
    if message.text == "Викторина без времени":
        quiz(message)
    elif message.text == "Блиц":
        quiz_with_timer(message)


def quiz(message: types.Message) -> None:
    """Forms from sends a quiz without time"""
    data = get_question_and_answers()
    msg = bot.send_poll(
        message.chat.id,
        type="quiz",
        question=data[0],
        options=data[1],
        correct_option_id=data[2],
        explanation=data[3],
        is_anonymous=False,
    )
    bot.register_next_step_handler(msg, blic_or_without_timer)


def quiz_with_timer(message: types.Message) -> None:
    """Forms and sends a quiz with a timer"""
    global total_points
    total_points += 1
    data = get_question_and_answers()
    msg = bot.send_poll(
        message.chat.id,
        type="quiz",
        question=data[0],
        options=data[1],
        correct_option_id=data[2],
        explanation=data[3],
        open_period=5,
        is_anonymous=False,
    )
    time_send = datetime.now().second
    time_end = time_send + 5
    while True:
        if time_send < time_end:
            while True:
                if total_responses(len(all_user_responses)) != total_points and time_send <= time_end:
                    time_send += 1
                    time.sleep(1)
                else:
                    while True:
                        if all_user_responses != [] and all_user_responses[-1] == data[2]:
                            correct_user_responses.append(all_user_responses[-1])
                            quiz_with_timer(message)
                        else:
                            bot.send_message(
                                message.chat.id,
                                text=f"В этот раз у тебя {len(correct_user_responses)} "
                                     f"правильных ответов подряд! \nЗнай, ты всегда можешь испытать себя снова!",
                            )
                            correct_user_responses.clear()
                            all_user_responses.clear()
                            total_points = 0
                            bot.register_next_step_handler(msg, blic_or_without_timer)
                        break
                    break
        else:
            bot.send_message(
                message.chat.id,
                text=f"Старайся успевать отвечать до того, как кончится время.\n "
            )
        break


def total_responses(*args):
    total = len(all_user_responses)
    return total


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer) -> None:
    all_user_responses.append(int(poll_answer.option_ids[0]))
    pass


if __name__ == "__main__":
    bot.polling()
