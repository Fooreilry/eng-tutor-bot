from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_options_keyboard(question: dict) -> InlineKeyboardBuilder:
    """Build inline keyboard for multiple_choice questions."""
    builder = InlineKeyboardBuilder()
    if question["options"]:
        for i, option in enumerate(question["options"]):
            builder.row(
                InlineKeyboardButton(text=option, callback_data=f"test_ans_{i}")
            )
    builder.row(
        InlineKeyboardButton(text="Не знаю ответа", callback_data="test_ans_skip")
    )
    return builder


def build_skip_keyboard() -> InlineKeyboardBuilder:
    """Build inline keyboard with skip button for text questions."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Не знаю ответа", callback_data="test_ans_skip")
    )
    return builder


def build_results_keyboard(passed: bool) -> InlineKeyboardBuilder:
    """Build keyboard for test results screen."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📋 Показать историю", callback_data="test_show_history"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="💬 Продолжить общение", callback_data="test_continue_chat"
        )
    )
    if not passed:
        builder.row(
            InlineKeyboardButton(
                text="⬇️ Понизить уровень", callback_data="test_downgrade"
            )
        )
    return builder
