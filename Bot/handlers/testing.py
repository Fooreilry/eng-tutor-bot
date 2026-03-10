import json
import random
from pathlib import Path

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Bot.keyboard import get_main_keyboard
from Bot.states import PlacementTest

testing_router = Router(name="Testing")

# Load questions from test.json
TEST_FILE = Path(__file__).parent.parent.parent / "test.json"
with open(TEST_FILE, "r", encoding="utf-8") as f:
    TEST_DATA = json.load(f)

QUESTIONS = TEST_DATA["questions"]

MAX_QUESTIONS = 10
# Threshold percentage to pass the test
PASS_THRESHOLD = 60

# Levels ordered from lowest to highest
LEVELS_ORDER = ["A1", "A2", "B1", "B2"]


def get_available_questions(user_level: str) -> list[dict]:
    """Get questions at or below the user's level."""
    level_index = LEVELS_ORDER.index(user_level)
    allowed_levels = LEVELS_ORDER[: level_index + 1]
    return [q for q in QUESTIONS if q["level"] in allowed_levels]


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


def format_question_text(question: dict, current: int, total: int) -> str:
    """Format question text with number and type hint."""
    q_type = question["type"]

    type_hints = {
        "multiple_choice": "Выбери правильный вариант:",
        "fill_in_the_blank": "Напиши ответ текстом:",
        "translate": "Напиши перевод текстом:",
        "error_correction": "Напиши исправленное предложение:",
        "word_order": "Напиши правильное предложение:",
    }
    hint = type_hints.get(q_type, "")

    return f"📝 Вопрос {current}/{total} [{question['level']}]\n\n{question['question']}\n\n{hint}"


def check_answer(question: dict, user_answer: str) -> bool:
    """Check if the user's answer is correct."""
    q_type = question["type"]
    clean = user_answer.strip().lower().rstrip(".")

    if q_type == "multiple_choice":
        return clean == question["answer"].strip().lower()

    if q_type == "translate":
        acceptable = question.get("acceptable_answers", [question["answer"]])
        return clean in [a.strip().lower().rstrip(".") for a in acceptable]

    # fill_in_the_blank, error_correction, word_order
    return clean == question["answer"].strip().lower().rstrip(".")


async def send_question(message: Message, state: FSMContext):
    """Send the current question to the user."""
    data = await state.get_data()
    questions = data["test_questions"]
    index = data["test_current"]
    total = len(questions)

    if index >= total:
        await finish_test(message, state)
        return

    question = questions[index]
    text = format_question_text(question, index + 1, total)

    if question["type"] == "multiple_choice":
        kb = build_options_keyboard(question)
        await message.answer(text, reply_markup=kb.as_markup())
    else:
        skip_kb = InlineKeyboardBuilder()
        skip_kb.row(
            InlineKeyboardButton(text="Не знаю ответа", callback_data="test_ans_skip")
        )
        await message.answer(text, reply_markup=skip_kb.as_markup())


async def process_answer(message_or_cb, state: FSMContext, user_answer: str | None):
    """Process the user's answer and move to the next question."""
    data = await state.get_data()
    questions = data["test_questions"]
    index = data["test_current"]
    history = data["test_history"]
    correct_count = data["test_correct"]

    question = questions[index]
    is_correct = check_answer(question, user_answer) if user_answer else False

    history.append(
        {
            "question": question["question"],
            "user_answer": user_answer or "Пропущено",
            "correct_answer": question["answer"],
            "is_correct": is_correct,
        }
    )

    if is_correct:
        correct_count += 1

    await state.update_data(
        test_current=index + 1,
        test_history=history,
        test_correct=correct_count,
    )

    # Determine which message object to use for sending
    if isinstance(message_or_cb, CallbackQuery):
        msg = message_or_cb.message
    else:
        msg = message_or_cb

    await send_question(msg, state)


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


async def finish_test(message: Message, state: FSMContext):
    """Show test results."""
    data = await state.get_data()
    correct = data["test_correct"]
    total = len(data["test_questions"])
    percentage = round(correct / total * 100)
    level = data.get("level", "A1")
    passed = percentage >= PASS_THRESHOLD

    if passed:
        result_text = (
            f"Yo, {data.get('name', 'buddy')}! Тест done! 🎉\n\n"
            f"Результат: {correct}/{total} ({percentage}%)\n\n"
            f"Ты точно определил свой уровень — {level}. "
            f"No cap, у тебя solid база! "
            f"Let's move on и начнём общаться?"
        )
    else:
        result_text = (
            f"Okay, {data.get('name', 'buddy')}, тест finished! 📊\n\n"
            f"Результат: {correct}/{total} ({percentage}%)\n\n"
            f"Looks like уровень {level} пока даётся нелегко. "
            f"Но hey, это не problem — можешь понизить level "
            f"или оставить как есть и принять challenge! 💪"
        )

    # Save results but keep state data for history viewing
    await state.update_data(test_passed=passed)
    await state.set_state(None)

    await message.answer(
        result_text, reply_markup=build_results_keyboard(passed).as_markup()
    )


# --- Handlers ---


@testing_router.callback_query(F.data == "start_testing")
async def start_testing(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    user_level = data.get("level", "A1")

    available = get_available_questions(user_level)
    selected = random.sample(available, min(MAX_QUESTIONS, len(available)))
    random.shuffle(selected)

    await state.update_data(
        test_questions=selected,
        test_current=0,
        test_history=[],
        test_correct=0,
    )
    await state.set_state(PlacementTest.in_progress)

    await cb.message.answer(
        "Let's do this! 🔥\n\n"
        f"У тебя будет {len(selected)} questions. "
        "Для multiple choice — жми кнопку, для остальных — пиши ответ текстом.\n\n"
        "Ready? Here we go!"
    )
    await send_question(cb.message, state)


@testing_router.callback_query(F.data == "skip_testing")
async def skip_testing(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    await cb.message.answer(
        "No problem! Можем пройти тест whenever you want. А пока — let's just chat!",
        reply_markup=get_main_keyboard(),
    )


@testing_router.callback_query(
    PlacementTest.in_progress, F.data.startswith("test_ans_")
)
async def handle_mc_answer(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    question = data["test_questions"][data["test_current"]]
    answer_part = cb.data.split("_")[-1]

    if answer_part == "skip":
        user_answer = None
    else:
        user_answer = question["options"][int(answer_part)]

    await process_answer(cb, state, user_answer)


@testing_router.message(PlacementTest.in_progress)
async def handle_text_answer(message: Message, state: FSMContext):
    await process_answer(message, state, message.text)


# --- Post-test actions ---


@testing_router.callback_query(F.data == "test_show_history")
async def show_history(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    history = data.get("test_history", [])

    if not history:
        await cb.message.answer("История тестирования пуста.")
        return

    lines = []
    for i, entry in enumerate(history, 1):
        icon = "✅" if entry["is_correct"] else "❌"
        lines.append(
            f"{i}. {entry['question']}\n"
            f"   Твой ответ: {entry['user_answer']} — "
            f"Правильный: {entry['correct_answer']} {icon}"
        )

    text = "📋 История ответов:\n\n" + "\n\n".join(lines)

    # Telegram message limit is 4096 chars, split if needed
    if len(text) <= 4096:
        await cb.message.answer(text)
    else:
        # Split into chunks
        for i in range(0, len(text), 4096):
            await cb.message.answer(text[i : i + 4096])


@testing_router.callback_query(F.data == "test_continue_chat")
async def continue_chat(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    name = data.get("name", "buddy")

    # Clear test data but keep user profile
    await state.update_data(
        test_questions=None,
        test_current=None,
        test_history=None,
        test_correct=None,
        test_passed=None,
    )

    await cb.message.answer(
        f"Alright {name}, let's vibe! 🤙\nЖми 'Начать диалог' когда будешь ready!",
        reply_markup=get_main_keyboard(),
    )


@testing_router.callback_query(F.data == "test_downgrade")
async def downgrade_level(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    current_level = data.get("level", "A1")
    name = data.get("name", "buddy")

    current_index = LEVELS_ORDER.index(current_level)
    if current_index > 0:
        new_level = LEVELS_ORDER[current_index - 1]
        await state.update_data(level=new_level)

        # Clear test data
        await state.update_data(
            test_questions=None,
            test_current=None,
            test_history=None,
            test_correct=None,
            test_passed=None,
        )

        await cb.message.answer(
            f"Got it, {name}! Я поменял твой level на {new_level}. "
            f"Don't worry, мы начнём с basics и будем level up together! 💪\n\n"
            "Жми 'Начать диалог' когда будешь ready!",
            reply_markup=get_main_keyboard(),
        )
    else:
        await cb.message.answer(
            f"{name}, ты уже на самом базовом уровне A1. "
            "Мы начнём с самого начала — it's all good!",
            reply_markup=get_main_keyboard(),
        )
