# Импортируем все модели, чтобы SQLAlchemy мог зарегистрировать их
from .bot import Bot
from .user import User
from .user_bot import UserBot

__all__ = ["Bot", "User", "UserBot"]
