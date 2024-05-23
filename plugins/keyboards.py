from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

class KeyboardDataClass:
    DELETE = ReplyKeyboardRemove
    menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Я на работе!", resize_keyboard=True, callback_data="in_job"),
            KeyboardButton(text="Я не на работе!", resize_keyboard=True, callback_data="not_in_job")
        ],
        [
            KeyboardButton(text="Моя статистика", resize_keyboard=True, callback_data="stat"),
            KeyboardButton(text="Информация о боте", resize_keyboard=True, callback_data="info"),
            KeyboardButton(text="Техподдержка", resize_keyboard=True, callback_data="tp")
        ]
    ])