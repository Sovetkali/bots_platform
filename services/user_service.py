from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models.user import User as UserModel
from core.models.db.user import User
from core.models.db.bot import Bot
from core.models.db.user_bot import UserBot

from core.repositories.user_repository import UserRepository
from core.repositories.bot_repository import BotRepository
from core.repositories.user_bot_repository import UserBotRepository

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_user_with_bot(self, user: UserModel, bot_code: str, bot_name: str):
        """
        Регистрирует пользователя и связывает его с ботом.
        Если пользователь уже существует, обновляет его данные и создает связь с ботом.
        """
        user_repo = UserRepository(self.session)
        bot_repo = BotRepository(self.session)
        user_bot_repo = UserBotRepository(self.session)

        # Получаем или создаем пользователя
        db_user = await user_repo.get_user_by_telegram_id(user.tg_id)
        if not db_user:
            db_user = await user_repo.create_user(user_id=user.tg_id, name=user.name, lang=user.lang)

        # Получаем или создаем бота
        bot = await bot_repo.create_bot_if_not_exists(bot_code, bot_name)

        # Создаем связь между пользователем и ботом
        user_bot = await user_bot_repo.link_user_to_bot(db_user.id, bot.id)

        # Если пользователь уже существовал, обновляем его данные
        if db_user.name != user.name or db_user.lang != user.lang:
            db_user.name = user.name
            db_user.lang = user.lang
            await self.session.flush()

        await self.session.commit()
        return db_user, bot, user_bot

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Получить пользователя по telegram_id"""
        user_repo = UserRepository(self.session)
        return await user_repo.get_user_by_telegram_id(telegram_id)

    async def get_user_bots(self, telegram_id: int) -> list[Bot]:
        """Получить список ботов, с которыми связан пользователь"""
        user_repo = UserRepository(self.session)
        user = await user_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            return []

        # Загружаем боты через связь
        await self.session.refresh(user, ["bots"])
        return user.bots
