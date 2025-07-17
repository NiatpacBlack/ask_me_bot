import re
import time

from telebot import types, TeleBot
from telebot.apihelper import ApiException
from telebot.types import ReplyKeyboardRemove

from ask_me_bot.questions.dataclasses import Question
from ask_me_bot.bot_keyboards import get_start_keyboard, inline_for_just_question, get_themes_keyboard
from questions.services import (
    get_question_and_answers,
    get_question_id_from_question_name,
    get_explanation_from_question,
    get_all_questions_from_db,
    get_random_question,
    get_detail_explanation_from_question, get_questions_by_theme_id, get_python_theme_id,
)
from config import BOT_TOKEN, BLITZ_TIMER, logger


bot = TeleBot(BOT_TOKEN)

total_points_in_blitz = 0
all_user_responses = []


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Displays a welcome message and start menu to the user."""
    try:
        # create_new_user_if_not_exist({
        #     "id": message.from_user.id,
        #     "username": message.from_user.username,
        #     "first_name": message.from_user.first_name,
        #     "last_name": message.from_user.last_name,
        # })
        bot.send_message(
            message.chat.id,
            text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:",
            reply_markup=get_start_keyboard(),
        )
    except (ApiException, KeyError):
        logger.error(ApiException)


@bot.message_handler(func=lambda m: m.text == "Простой вопрос Python")
def send_just_question_python(message: types.Message) -> None:
    """Sends question with no answer options by Python topics."""
    try:
        python_theme_id = get_python_theme_id()
        if not python_theme_id:
            raise ApiException

        _send_just_question(
            get_random_question(
                get_questions_by_theme_id(python_theme_id)
            ),
            message,
        )
    except ApiException:
        logger.error(ApiException)


@bot.message_handler(func=lambda m: m.text == "Простой вопрос")
def send_just_question(message: types.Message) -> None:
    """Sends question with no answer options."""
    try:
        _send_just_question(
            get_random_question(
                get_all_questions_from_db(by="just_question")
            ),
            message,
        )
    except ApiException:
        logger.error(ApiException)


@bot.message_handler(func=lambda m: m.text == "Простой вопрос по теме")
def send_just_question_by_theme(message: types.Message) -> None:
    """Sends question with no answer options by theme."""
    try:
        bot.send_message(
            message.chat.id,
            text="Выберите тему:",
            reply_markup=get_themes_keyboard(),
        )
    except ApiException:
        logger.error(ApiException)


@bot.message_handler(func=lambda m: m.text == "Квиз вопрос")
def send_quiz(message: types.Message) -> None:
    """Sends the user a quiz with a question."""
    try:
        _send_quiz(
            get_question_and_answers(),
            message,
            reply_markup=get_start_keyboard(),
        )
    except ApiException:
        logger.error(ApiException)


@bot.message_handler(func=lambda m: m.text == "Блиц")
def send_blitz_quiz(message: types.Message) -> None:
    """Starts a user poll blitz. Sends the user questions for the time before the first error."""
    global total_points_in_blitz
    _clear_global_variables()

    try:
        index_current_answer = _send_quiz(
            get_question_and_answers(),
            message,
            with_period=BLITZ_TIMER,
            reply_markup=ReplyKeyboardRemove(),
        )

        time_start = 0

        while time_start < BLITZ_TIMER:

            # if the user answered the question
            if len(all_user_responses) == total_points_in_blitz + 1:
                if all_user_responses[-1] == index_current_answer:
                    total_points_in_blitz += 1

                    index_current_answer = _send_quiz(
                        get_question_and_answers(), message, with_period=BLITZ_TIMER
                    )

                    time_start = 0
                else:
                    _send_blitz_over_message(message.chat.id)
                    _clear_global_variables()
                    return None

            # if the question was not answered
            else:
                time_start += 1
                time.sleep(1)

        _send_blitz_timeout_message(message.chat.id)
        _clear_global_variables()
    except ApiException:
        logger.error(ApiException)


@bot.callback_query_handler(func=lambda call: re.match(r"explanation", call.data))
def callback_inline_explanation(call):
    try:
        question_id = call.data.replace("explanation", "")
        explanation = get_explanation_from_question(question_id)
        bot.send_message(call.message.chat.id, text=explanation)
    except ApiException:
        logger.error(ApiException)


@bot.callback_query_handler(
    func=lambda call: re.match(r"detail_explanation", call.data)
)
def callback_inline_detail_explanation(call):
    try:
        question_id = call.data.replace("detail_explanation", "")
        detail_explanation = get_detail_explanation_from_question(question_id)
        bot.send_message(call.message.chat.id, text=detail_explanation)
    except ApiException:
        logger.error(ApiException)


@bot.callback_query_handler(func=lambda call: re.match(r"just_question_theme", call.data))
def callback_inline_theme_for_just_question(call):
    try:
        theme_id = call.data.replace("just_question_theme", "")
        _send_just_question(
            get_random_question(
                get_questions_by_theme_id(theme_id)
            ),
            call.message,
        )
    except ApiException:
        logger.error(ApiException)


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer) -> None:
    """Handler for handling survey responses."""
    all_user_responses.append(int(poll_answer.option_ids[0]))


def _send_quiz(data, message: types.Message, with_period=None, reply_markup=None) -> int:
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
            reply_markup=reply_markup,
        )
    except ApiException:
        logger.error(ApiException)

    return data.index_current_answer


def _send_just_question(data: Question, message: types.Message) -> None:
    """Question with no answer options"""
    try:
        question_id = get_question_id_from_question_name(data.question_name)
        bot.send_message(
            message.chat.id,
            data.question_name,
            reply_markup=inline_for_just_question(question_id),
        )
    except ApiException:
        logger.error(ApiException)


def _send_blitz_over_message(chat_id: int) -> None:
    """Sends a message to a user who has finished a blitz poll."""
    try:
        bot.send_message(
            chat_id,
            text=f"В этот раз у тебя {total_points_in_blitz} "
                 f"правильных ответов подряд! \nЗнай, ты всегда можешь испытать себя снова!",
            reply_markup=get_start_keyboard(),
        )
    except ApiException:
        logger.error(ApiException)


def _send_blitz_timeout_message(chat_id: int) -> None:
    """Sends a message to a user who has run out of time during a blitz poll."""
    try:
        bot.send_message(
            chat_id,
            text=f"Старайся успевать отвечать до того, как кончится время.\n "
                 f"У тебя {total_points_in_blitz} правильных ответов из {total_points_in_blitz + 1}",
            reply_markup=get_start_keyboard(),
        )
    except ApiException:
        logger.error(ApiException)


def _clear_global_variables() -> None:
    global total_points_in_blitz
    all_user_responses.clear()
    total_points_in_blitz = 0


if __name__ == "__main__":
    import requests
    while True:
        try:
            bot.polling(timeout=60)
            break
        except requests.exceptions.ReadTimeout:
            continue
