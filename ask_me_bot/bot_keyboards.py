from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from ask_me_bot.questions.services import get_detail_explanation_from_question


def get_start_keyboard() -> ReplyKeyboardMarkup:
    """Returns the buttons that drop down at the start of the bot."""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Простой вопрос"))
    keyboard.add(types.KeyboardButton(text="Квиз вопрос"))
    keyboard.add(types.KeyboardButton(text="Блиц"))
    return keyboard


def inline_for_just_question(question_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Объяснение", callback_data=f"explanation{question_id}"))
    if get_detail_explanation_from_question(question_id):
        markup.add(InlineKeyboardButton(text="Подробное объяснение", callback_data=f"detail_explanation{question_id}"))
    return markup
