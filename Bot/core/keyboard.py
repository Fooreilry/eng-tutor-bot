from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Button text constants
BTN_CHAT = "💬 Начать диалог"
BTN_WORD_OF_DAY = "🔤 Слово дня"
BTN_TASKS = "📝 Задания"
BTN_DICTIONARY = "📖 Мой словарь"
BTN_PROFILE = "👤 Профиль"


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Main reply keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CHAT), KeyboardButton(text=BTN_WORD_OF_DAY)],
            [KeyboardButton(text=BTN_TASKS), KeyboardButton(text=BTN_DICTIONARY)],
            [KeyboardButton(text=BTN_PROFILE)],
        ],
        resize_keyboard=True,
    )
