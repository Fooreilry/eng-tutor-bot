from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_level_keyboard() -> InlineKeyboardBuilder:
    """Inline keyboard for English level selection"""
    builder = InlineKeyboardBuilder()
    levels = [
        ("A1 - Beginner", "level_a1"),
        ("A2 - Elementary", "level_a2"),
        ("B1 - Intermediate", "level_b1"),
        ("B2 - Upper-Intermediate", "level_b2"),
    ]
    for text, callback in levels:
        builder.row(InlineKeyboardButton(text=text, callback_data=callback))
    return builder


def get_skip_keyboard() -> InlineKeyboardBuilder:
    """Inline keyboard with skip button"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Skip", callback_data="skip_additional"))
    return builder


def get_testing_keyboard() -> InlineKeyboardBuilder:
    """Inline keyboard for testing offer"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Yep, let's go!", callback_data="start_testing"),
        InlineKeyboardButton(text="Nah, later", callback_data="skip_testing"),
    )
    return builder
