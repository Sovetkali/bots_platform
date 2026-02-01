from core.database import db
from core.repositories.user_repository import UserRepository
from core.base.service import BotService
from core.models.user import User
from core.models.message import Message
from core.keyboard_templates import SimpleTemplate, MenuTemplate, ActionTemplate

class ServiceBotService(BotService):
    def __init__(self):
        # Основное меню с использованием шаблона
        self.main_menu = SimpleTemplate([
            {"text": "⚙️ Настройки", "callback_data": "settings:open"},
            {"text": "❓ Помощь", "callback_data": "help"}
        ])

        # Меню настроек
        self.settings_menu = MenuTemplate(
            items=[
                {"text": "🔔 Уведомления", "callback_data": "settings:notifications"},
                {"text": "🌐 Язык", "callback_data": "settings:language"},
                {"text": "🔒 Безопасность", "callback_data": "settings:security"}
            ],
            back_button={"text": "← Назад", "callback_data": "main_menu"}
        )

        # Кнопки подтверждения
        self.confirm_action = ActionTemplate(
            confirm_text="✅ Подтвердить",
            cancel_text="❌ Отменить",
            confirm_data="action_confirm",
            cancel_data="action_cancel"
        )

    async def register_user(self, user: User):
        async with db.session() as session:
            user_repo = UserRepository(session)

            new_user = await user_repo.create_user(user_id=user.id, name=user.name, lang=user.lang)

            await session.commit()
            return new_user

    async def start(self, user: User) -> str:
        return f"Привет, {user.name}!\nТвой user_id: <code>{user.id}</code>\nЯзык: {user.lang}"

    async def echo_message(self, msg: Message) -> str:
        return f"Эхо ответ:\nID-чата: <code>{msg.chat_id}</code>\nID-сообщения: <code>{msg.msg_id}</code>\nДата создания: {msg.date}\nТекст: {msg.text}"

    def get_keyboard(self, menu_type: str = "main", **context):
        """Получить клавиатуру по типу меню с поддержкой контекста"""
        if menu_type == "main":
            return self.main_menu.build(**context)
        elif menu_type == "settings":
            return self.settings_menu.build(**context)
        elif menu_type == "confirm":
            return self.confirm_action.build(**context)
        else:
            return self.main_menu.build(**context)
