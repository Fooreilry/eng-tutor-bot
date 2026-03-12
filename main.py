import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from Bot.modules.acquaintance import router as acquaintance_router
from Bot.modules.quiz import router as quiz_router
from Bot.modules.chat import router as chat_router
from Bot.modules.menu import router as menu_router

load_dotenv()

bot_key = os.getenv("T_BOT_KEY")

bot = Bot(token=bot_key)
disp = Dispatcher()


async def main():
    try:
        print("Старт программы...")
        disp.include_router(acquaintance_router)
        disp.include_router(quiz_router)
        disp.include_router(chat_router)
        disp.include_router(menu_router)
        await disp.start_polling(bot)
        print("Успешный запуск!")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
