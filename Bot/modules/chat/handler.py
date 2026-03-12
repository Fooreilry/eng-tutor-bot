from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Bot.core.keyboard import (
    BTN_CHAT,
    BTN_DICTIONARY,
    BTN_PROFILE,
    BTN_TASKS,
    BTN_WORD_OF_DAY,
    get_main_keyboard,
)
from Bot.modules.chat.states import ChatWithAlex
from Gemini.agent import chat_with_alex

router = Router(name="Chat")

MENU_BUTTONS = {BTN_CHAT, BTN_WORD_OF_DAY, BTN_TASKS, BTN_DICTIONARY, BTN_PROFILE}


@router.message(F.text == BTN_CHAT)
async def start_chat(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", message.from_user.first_name)

    if not data.get("level"):
        await message.answer(
            "Yo, мы ещё не познакомились! Нажми /start чтобы начать."
        )
        return

    await state.update_data(chat_history=[])
    await state.set_state(ChatWithAlex.active)

    await message.answer(
        f"Let's chat, {name}! 🤙\n"
        "Пиши мне что угодно — можем поболтать, попрактиковать English, "
        "или just hang out. Напиши /stop чтобы выйти из чата."
    )


@router.message(ChatWithAlex.active, F.text.startswith("/stop"))
async def stop_chat(message: Message, state: FSMContext):
    await state.update_data(chat_history=[])
    await state.set_state(None)

    await message.answer(
        "Alright, was fun chatting! Возвращаемся в меню 🤙",
        reply_markup=get_main_keyboard(),
    )


@router.message(ChatWithAlex.active, F.text.in_(MENU_BUTTONS))
async def menu_button_in_chat(message: Message, state: FSMContext):
    """Если нажали кнопку меню — выходим из чата, показываем меню"""
    await state.update_data(chat_history=[])
    await state.set_state(None)
    await message.answer(
        "Okay, вышел из чата! 👋",
        reply_markup=get_main_keyboard(),
    )


@router.message(ChatWithAlex.active)
async def handle_chat_message(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Yo, я пока only text понимаю! Напиши что-нибудь 📝")
        return

    data = await state.get_data()
    name = data.get("name", message.from_user.first_name)
    level = data.get("level", "A1")
    interests = data.get("interests", "")
    additional = data.get("additional")
    history = data.get("chat_history", [])

    try:
        response = await chat_with_alex(
            message=message.text,
            history=history,
            name=name,
            level=level,
            interests=interests,
            additional=additional,
        )

        history.append({"role": "user", "text": message.text})
        history.append({"role": "model", "text": response})
        if len(history) > 20:
            history = history[-20:]

        await state.update_data(chat_history=history)
        await message.answer(response)

    except Exception as e:
        print(f"Gemini error: {e}")
        await message.answer(
            "Oops, something went wrong on my end 😅 Try again in a sec!"
        )
