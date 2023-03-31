from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


def get_start_keyboard() -> ReplyKeyboardMarkup:
    """Returns the buttons that drop down at the start of the bot."""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Простой вопрос"))
    keyboard.add(types.KeyboardButton(text="Квиз вопрос"))
    keyboard.add(types.KeyboardButton(text="Блиц"))
    return keyboard


def inline_for_question(question_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Объяснение", callback_data=f"just_question{question_id}"))
    return markup
