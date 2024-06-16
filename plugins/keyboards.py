from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

class KeyboardDataClass:
    DELETE = ReplyKeyboardRemove
    menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Я на работе!", callback_data="in_job"),
            KeyboardButton(text="Узнать статус")
            KeyboardButton(text="Я не на работе!", callback_data="not_in_job")
        ],
        [
            KeyboardButton(text="Моя статистика", callback_data="stat"),
            KeyboardButton(text="Информация о боте", callback_data="info"),
            KeyboardButton(text="Техподдержка", callback_data="tp")
        ]
    ], resize_keyboard=True)