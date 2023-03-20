from telebot import types


def get_start_keyboard():
    """Returns the buttons that drop down at the start of the bot."""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Получить задачу"))
    keyboard.add(types.KeyboardButton(text="Блиц"))
    return keyboard
