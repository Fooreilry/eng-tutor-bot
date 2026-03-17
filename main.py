import asyncio

from aiogram import Bot, Dispatcher

from Bot.modules.acquaintance import router as acquaintance_router
from Bot.modules.quiz import router as quiz_router
from Bot.modules.chat import router as chat_router
from Bot.modules.menu import router as menu_router
from core.config import config
from core.database import init_db
from core.middleware import DatabaseMiddleware




async def main():
    try:
        print("Старт программы...")

        await init_db()

        bot = Bot(token=config.telegram_token)
        disp = Dispatcher()

        disp.update.middleware(DatabaseMiddleware())

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
