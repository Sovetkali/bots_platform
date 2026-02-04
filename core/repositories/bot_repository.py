from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.db.bot import Bot

class BotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_bot_by_code(self, bot_code: str) -> Bot | None:
        """Получить бота по коду"""
        result = await self.session.execute(
            select(Bot).where(Bot.code == bot_code)
        )
        return result.scalar_one_or_none()

    async def create_bot_if_not_exists(self, bot_code: str, bot_name: str) -> Bot:
        """Создать бота, если он не существует"""
        bot = await self.get_bot_by_code(bot_code)
        if not bot:
            bot = Bot(code=bot_code, name=bot_name)
            self.session.add(bot)
            await self.session.flush()
        return bot
