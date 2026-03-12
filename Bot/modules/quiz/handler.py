import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Bot.core.keyboard import get_main_keyboard
from Bot.modules.quiz.keyboard import (
    build_options_keyboard,
    build_results_keyboard,
    build_skip_keyboard,
)
from Bot.modules.quiz.service import (
    LEVELS_ORDER,
    MAX_QUESTIONS,
    PASS_THRESHOLD,
    check_answer,
    format_question_text,
    get_available_questions,
)
from Bot.modules.quiz.states import PlacementTest

router = Router(name="Quiz")


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
        await message.answer(text, reply_markup=build_skip_keyboard().as_markup())


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

    if isinstance(message_or_cb, CallbackQuery):
        msg = message_or_cb.message
    else:
        msg = message_or_cb

    await send_question(msg, state)


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

    await state.update_data(test_passed=passed)
    await state.set_state(None)

    await message.answer(
        result_text, reply_markup=build_results_keyboard(passed).as_markup()
    )


# --- Handlers ---


@router.callback_query(F.data == "start_testing")
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


@router.callback_query(F.data == "skip_testing")
async def skip_testing(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    await cb.message.answer(
        "No problem! Можем пройти тест whenever you want. А пока — let's just chat!",
        reply_markup=get_main_keyboard(),
    )


@router.callback_query(
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


@router.message(PlacementTest.in_progress)
async def handle_text_answer(message: Message, state: FSMContext):
    await process_answer(message, state, message.text)


# --- Post-test actions ---


@router.callback_query(F.data == "test_show_history")
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

    if len(text) <= 4096:
        await cb.message.answer(text)
    else:
        for i in range(0, len(text), 4096):
            await cb.message.answer(text[i : i + 4096])


@router.callback_query(F.data == "test_continue_chat")
async def continue_chat(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    name = data.get("name", "buddy")

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


@router.callback_query(F.data == "test_downgrade")
async def downgrade_level(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    data = await state.get_data()
    current_level = data.get("level", "A1")
    name = data.get("name", "buddy")

    current_index = LEVELS_ORDER.index(current_level)
    if current_index > 0:
        new_level = LEVELS_ORDER[current_index - 1]
        await state.update_data(level=new_level)

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
