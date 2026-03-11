from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Bot.keyboard import BTN_PROFILE, BTN_WORD_OF_DAY, BTN_DICTIONARY, BTN_TASKS

menu_router = Router(name="Menu")


@menu_router.message(F.text == BTN_PROFILE)
async def show_profile(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", message.from_user.first_name)
    level = data.get("level", "не определён")
    interests = data.get("interests", "не указаны")

    await message.answer(
        f"👤 Your profile, {name}:\n\n"
        f"📊 Level: {level}\n"
        f"🎯 Interests: {interests}\n\n"
        "Keep learning и level up! 💪"
    )


@menu_router.message(F.text == BTN_WORD_OF_DAY)
async def word_of_the_day(message: Message, state: FSMContext):
    # TODO: подключить реальную выборку слов
    await message.answer(
        "🔤 Word of the Day\n\n"
        "**vibe** /vaɪb/\n"
        "— атмосфера, настроение\n\n"
        "\"This place has a really cool vibe.\"\n\n"
        "Скоро тут будет personalized word каждый день — stay tuned! 🤙"
    )


@menu_router.message(F.text == BTN_DICTIONARY)
async def show_dictionary(message: Message, state: FSMContext):
    # TODO: подключить словарь из БД
    await message.answer(
        "📖 Твой словарь пока пуст.\n\n"
        "Как начнём общаться, я буду сохранять new words сюда. "
        "Потом сможешь повторять их в любое время!"
    )


@menu_router.message(F.text == BTN_TASKS)
async def show_tasks(message: Message, state: FSMContext):
    # TODO: генерация заданий
    data = await state.get_data()
    name = data.get("name", "buddy")

    await message.answer(
        f"📝 Задания на сегодня, {name}:\n\n"
        "Скоро тут появятся daily tasks — "
        "слова для повторения, мини-упражнения и challenges. "
        "For now, just chat with me! 😎"
    )
