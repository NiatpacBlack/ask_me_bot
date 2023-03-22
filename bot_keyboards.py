from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard():
    """Returns the buttons that drop down at the start of the bot."""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Вопрос без вариантов"))
    keyboard.add(types.KeyboardButton(text="Получить задачу"))
    keyboard.add(types.KeyboardButton(text="Блиц"))
    return keyboard


def inline_for_question(data):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Объяснение", callback_data=data.explanation))
    return markup
