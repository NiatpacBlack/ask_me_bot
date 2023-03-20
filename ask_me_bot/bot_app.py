import time
import traceback
from loguru import logger

from telebot import types, TeleBot
from telebot.apihelper import ApiException

from bot_keyboards import get_start_keyboard
from questions.services import get_question_and_answers
from config import BOT_TOKEN, BLITZ_TIMER


bot = TeleBot(BOT_TOKEN)

total_points_in_blitz = 0
all_user_responses = []


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Displays a welcome message and start menu to the user."""
    try:
        bot.send_message(
            message.chat.id,
            text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:",
            reply_markup=get_start_keyboard(),
        )
    except ApiException:
        logger.error(traceback.format_exc())


def send_quiz(data, message: types.Message, with_period=None) -> int:
    """Send a quiz to a user with a question."""
    try:
        bot.send_poll(
            message.chat.id,
            type="quiz",
            question=data.question_name,
            options=data.answers,
            correct_option_id=data.index_current_answer,
            explanation=data.explanation,
            is_anonymous=False,
            open_period=with_period,
        )
    except ApiException:
        logger.error(traceback.format_exc())

    return data.index_current_answer


@bot.message_handler(func=lambda m: m.text == "Получить задачу")
def send_question(message: types.Message) -> None:
    """Sends the user a quiz with a question."""
    try:
        send_quiz(get_question_and_answers(), message)
    except ApiException:
        logger.error(traceback.format_exc())


@bot.message_handler(func=lambda m: m.text == "Блиц")
def send_blitz_question(message: types.Message) -> None:
    """Starts a user poll blitz. Sends the user questions for the time before the first error."""
    global total_points_in_blitz
    _clear_global_variables()

    try:
        index_current_answer = send_quiz(get_question_and_answers(), message, with_period=BLITZ_TIMER)

        time_start = 0

        while time_start < BLITZ_TIMER:
            if len(all_user_responses) == total_points_in_blitz + 1:
                if all_user_responses[-1] == index_current_answer:
                    total_points_in_blitz += 1
                    index_current_answer = send_quiz(get_question_and_answers(), message, with_period=BLITZ_TIMER)
                    time_start = 0
                else:
                    _send_blitz_over_message(message.chat.id)
                    _clear_global_variables()
                    return None
            else:
                time_start += 1
                time.sleep(1)

        _send_blitz_timeout_message(message.chat.id)
        _clear_global_variables()
    except ApiException:
        logger.error(traceback.format_exc())


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer) -> None:
    """Handler for handling survey responses."""
    all_user_responses.append(int(poll_answer.option_ids[0]))


def _send_blitz_over_message(chat_id: int) -> None:
    """Sends a message to a user who has finished a blitz poll."""
    try:
        bot.send_message(
            chat_id,
            text=f"В этот раз у тебя {total_points_in_blitz} "
                 f"правильных ответов подряд! \nЗнай, ты всегда можешь испытать себя снова!",
        )
    except ApiException:
        logger.error(traceback.format_exc())


def _send_blitz_timeout_message(chat_id: int) -> None:
    """Sends a message to a user who has run out of time during a blitz poll."""
    try:
        bot.send_message(
            chat_id,
            text=f"Старайся успевать отвечать до того, как кончится время.\n "
                 f"У тебя {total_points_in_blitz} правильных ответов из {total_points_in_blitz + 1}"
        )
    except ApiException:
        logger.error(traceback.format_exc())


def _clear_global_variables() -> None:
    global total_points_in_blitz
    all_user_responses.clear()
    total_points_in_blitz = 0


if __name__ == "__main__":
    bot.polling()
