from aiogram import Router
from aiogram.types import Message, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

acquaintance_router = Router(name="Acquaintance")

@acquaintance_router.message(Command("start"))
async def message_handler(message: Message):


    await message.answer(f"Hi {message.from_user.full_name} 👋!")
    await message.answer("My name is Alex. Yor persona English tutor")

    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="About you!"))
    builder.row(KeyboardButton(text="About me?"))

    await message.answer("How you start our dialogue?", reply_markup=builder.as_markup(resize_keyboard=True))

