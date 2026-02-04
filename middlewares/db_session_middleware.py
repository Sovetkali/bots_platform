from aiogram import BaseMiddleware
from core.database import db

class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with db.session() as session:
            data["db_session"] = session
            return await handler(event, data)
