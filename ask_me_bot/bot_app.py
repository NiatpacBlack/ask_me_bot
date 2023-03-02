import time

import telebot
from telebot import TeleBot, types

from questions.services import get_question_and_answers
from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)

correct_answer_counter = 0


@bot.message_handler(commands=["start"])
def start(message) -> None:
    """Displays a welcome message and start menu to the user."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Викторина без времени")
    btn2 = types.KeyboardButton("Блиц")
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        text=f"Здравствуйте, {message.from_user.full_name}, выберите действие:", reply_markup=markup)
    bot.clear_step_handler(message)


@bot.message_handler(content_types=['text'])
def blic_or_without_timer(message):
    """Depending on the user's choice, sends him either a quiz with or without time"""
    if message.text == 'Викторина без времени':
        quiz_without_timer(message)
    elif message.text == 'Блиц':
        quiz_with_timer_runs_until_the_first_wrong_answer(message)


@bot.message_handler(content_types=['text'])
def quiz_without_timer(message: types.Message) -> None:
    """Forms from sends a quiz without time"""
    data = get_question_and_answers()
    if message.text == 'Викторина без времени':
        bot.send_poll(message.chat.id,
                      type='quiz',
                      question=data[0],
                      options=data[1],
                      correct_option_id=data[2],
                      explanation=data[3],
                      is_anonymous=False,
                      )


def quiz_with_timer_runs_until_the_first_wrong_answer(message):
    """Forms and sends a quiz with a timer"""
    global data
    data = get_question_and_answers()
    bot.send_poll(message.chat.id,
                  type='quiz',
                  question=data[0],
                  options=data[1],
                  correct_option_id=data[2],
                  explanation=data[3],
                  open_period=15,
                  is_anonymous=False
                  ).message_id

    @bot.poll_answer_handler()
    def handle_poll_answer(pollAnswer):  # pollAnswer stores user data and his answer to QUIZ
        """We fix the selected user's answer in the BLIT mode.
           If the answer is correct, we immediately send him the next QUIZ.
           And so on until the first wrong answer"""
        if int(pollAnswer.option_ids[0]) == data[2]: # Compare the selected user answer with the correct answer from the database
            global correct_answer_counter
            correct_answer_counter += 1
            quiz_with_timer_runs_until_the_first_wrong_answer(message)
        else:
            print('else')
            bot.send_message(
            message.from_user.id,
            text=f"В этот раз {pollAnswer.user.username} у тебя {correct_answer_counter} правильных ответов подряд")

            # Unfinished block:
            # It is necessary to make it so that after the completion of the blitz, the user is redirected to the main menu

            # Possible Methods:
            # bot.stop_poll()
            # bot.delete_message()


if __name__ == '__main__':
    bot.polling()

