from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.db.user_bot import UserBot

class UserBotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def link_user_to_bot(self, user_id: int, bot_id: int) -> UserBot:
        """Создать связь между пользователем и ботом"""
        # Проверяем, существует ли уже такая связь
        result = await self.session.execute(
            select(UserBot).where(
                UserBot.user_id == user_id,
                UserBot.bot_id == bot_id
            )
        )
        existing_link = result.scalar_one_or_none()

        if not existing_link:
            link = UserBot(user_id=user_id, bot_id=bot_id)
            self.session.add(link)
            await self.session.flush()
            return link

        return existing_link
