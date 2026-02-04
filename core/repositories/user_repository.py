from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.db.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, *, user_id: int, name: str, lang: str) -> User:
        user = User(telegram_id=user_id, name=name, lang=lang)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Получить пользователя по telegram_id"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
