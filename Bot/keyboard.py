from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Main reply keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать диалог")]
        ],
        resize_keyboard=True
    )