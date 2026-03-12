from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Bot.core.keyboard import get_main_keyboard
from Bot.modules.acquaintance.keyboard import (
    get_level_keyboard,
    get_skip_keyboard,
    get_testing_keyboard,
)
from Bot.modules.acquaintance.states import UserRegistration

router = Router(name="Acquaintance")


# --- Start command ---


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(f"Yo, {message.from_user.first_name}! What's good?")
    await message.answer(
        "Я Alex, твой new buddy из Нью-Йорка. "
        "Буду помогать тебе with English, но не как скучный teacher, "
        "а как real friend, you know?"
    )

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="А ты кто такой?", callback_data="about_alex")
    )
    builder.row(
        InlineKeyboardButton(text="Давай расскажу о себе", callback_data="about_user")
    )

    await message.answer(
        "So, с чего начнём? Хочешь узнать обо мне или сразу познакомимся?",
        reply_markup=builder.as_markup(),
    )


# --- About Alex ---


@router.callback_query(F.data == "about_alex")
async def about_alex(cb: CallbackQuery):
    await cb.answer()

    await cb.message.answer(
        "Okay, quick intro about me!\n\n"
        "Мне 22, я из NYC — born and raised. "
        "Люблю hip-hop, Netflix shows и memes (who doesn't, right?). "
        "Английский для меня native, но я понимаю как это — учить новый язык."
    )
    await cb.message.answer(
        "Я не буду грузить тебя grammar rules и boring exercises. "
        "Мы просто будем vibe together, общаться, играть в игры, "
        "и ты сам не заметишь как заговоришь like a pro."
    )

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Sounds cool! Расскажу о себе", callback_data="about_user"
        )
    )

    await cb.message.answer(
        "Now your turn — tell me about yourself?", reply_markup=builder.as_markup()
    )


# --- User registration flow ---


@router.callback_query(F.data == "about_user")
async def start_registration(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    await cb.message.answer(
        "Nice, давай знакомиться! First things first — "
        "как тебя зовут? Можешь написать как хочешь, чтобы я тебя называл."
    )

    await state.set_state(UserRegistration.name)


@router.message(UserRegistration.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)

    await message.answer(f"{name}! Cool name, I like it.")
    await message.answer(
        "Теперь расскажи, какой у тебя сейчас level английского? "
        "Не парься если не знаешь точно — выбери примерно, потом разберёмся.",
        reply_markup=get_level_keyboard().as_markup(),
    )

    await state.set_state(UserRegistration.level)


@router.callback_query(UserRegistration.level, F.data.startswith("level_"))
async def process_level(cb: CallbackQuery, state: FSMContext):
    await cb.answer()

    level_map = {
        "level_a1": "A1",
        "level_a2": "A2",
        "level_b1": "B1",
        "level_b2": "B2",
    }
    level = level_map.get(cb.data, "A1")
    await state.update_data(level=level)

    level_responses = {
        "A1": "Beginner? No worries, мы все с чего-то начинали! I got you.",
        "A2": "Elementary — nice! У тебя уже есть база, будем building on that.",
        "B1": "Intermediate, cool! Значит можем уже нормально общаться на English.",
        "B2": "Upper-Intermediate? Impressive! Будем polishing твой English до идеала.",
    }

    await cb.message.answer(level_responses.get(level, "Got it!"))
    await cb.message.answer(
        "Now tell me — what are you into? Музыка, сериалы, games, sports? "
        "Напиши через запятую what you like, так мне будет проще подбирать темы для нас."
    )

    await state.set_state(UserRegistration.interests)


@router.message(UserRegistration.interests)
async def process_interests(message: Message, state: FSMContext):
    interests = message.text.strip()
    await state.update_data(interests=interests)

    await message.answer(
        f"О, {interests.split(',')[0].strip()}? That's dope! "
        "У нас будет много о чём поговорить."
    )
    await message.answer(
        "Last question — может хочешь что-то ещё добавить о себе? "
        "Любые details которые помогут мне лучше тебя понять. "
        "Или можешь skip, if you want.",
        reply_markup=get_skip_keyboard().as_markup(),
    )

    await state.set_state(UserRegistration.additional)


@router.callback_query(
    UserRegistration.additional, F.data == "skip_additional"
)
async def skip_additional(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(additional=None)
    await finish_registration(cb.message, state)


@router.message(UserRegistration.additional)
async def process_additional(message: Message, state: FSMContext):
    additional = message.text.strip()
    await state.update_data(additional=additional)
    await finish_registration(message, state)


async def finish_registration(message: Message, state: FSMContext):
    """Complete registration and show user data"""
    data = await state.get_data()

    print("\n" + "=" * 50)
    print("NEW USER REGISTERED:")
    print(f"  Name: {data.get('name')}")
    print(f"  Level: {data.get('level')}")
    print(f"  Interests: {data.get('interests')}")
    print(f"  Additional: {data.get('additional', 'Not provided')}")
    print("=" * 50 + "\n")

    prompt_info = f"""
User Profile:
- Name: {data.get("name")}
- English Level: {data.get("level")}
- Interests: {data.get("interests")}
- Additional Info: {data.get("additional") or "None"}
"""
    print("PROMPT INFO:")
    print(prompt_info)

    await state.set_state(None)

    await message.answer(
        f"Alright {data.get('name')}, I got everything! "
        "Теперь я знаю тебя немного лучше."
    )

    level = data.get("level", "A1")

    if level == "A1":
        await message.answer(
            "Мы начнём with the basics — step by step, no rush! "
            "Let's just chat and have fun! 🤙",
            reply_markup=get_main_keyboard(),
        )
    else:
        await message.answer(
            "By the way, хочешь пройти quick test чтобы я точнее понял твой level? "
            "Это займёт just a few minutes. No pressure though!",
            reply_markup=get_testing_keyboard().as_markup(),
        )
