import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from Bot.handlers.acquaintance import acquaintance_router
from Bot.handlers.menu import menu_router
from Bot.handlers.testing import testing_router
from Gemini.client import client

load_dotenv()

bot_key = os.getenv("T_BOT_KEY")

bot = Bot(token=bot_key)
disp = Dispatcher()


async def main():
    try:
        print("Старт программы...")
        disp.include_router(acquaintance_router)
        disp.include_router(testing_router)
        disp.include_router(menu_router)
        await disp.start_polling(bot)
        print("Успешный запуск!")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # response = client.models.generate_content(
    #     model="gemini-3-flash-preview",
    #     contents="Explain how AI works in a few words",
    # )

    # print(response)
    asyncio.run(main())
