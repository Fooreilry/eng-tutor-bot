from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from core.database import AsyncSessionFactory


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict], Awaitable[Any]],
            event: TelegramObject,
            data: dict,
    ) -> Any:
        async with AsyncSessionFactory() as session:
            data["session"] = session
            return await handler(event, data)
