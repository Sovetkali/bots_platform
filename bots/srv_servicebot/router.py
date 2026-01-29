from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.base.router import BotRouter
from .service import ServiceBotService
from core.models.user import User as UserContext
from core.models.message import Message as MessageContext
from utils.logger import logger

class ServiceBotRouter(BotRouter):
    def __init__(self, service: ServiceBotService):
        self._router = Router()
        self._service = service
        self._register()

    def _register(self):
        self._router.message.register(self.start, Command("start"))
        self._router.message.register(self.message_handler)

        # Регистрация обработчиков callback от кнопок
        self._router.callback_query.register(self.handle_main_menu, F.data == "start")
        self._router.callback_query.register(self.handle_settings_open, F.data == "settings:open")
        self._router.callback_query.register(self.handle_help, F.data == "help")
        self._router.callback_query.register(self.handle_settings_menu, F.data.startswith("settings:"))
        self._router.callback_query.register(self.handle_main_menu_back, F.data == "main_menu")
        self._router.callback_query.register(self.handle_action_confirm, F.data == "action_confirm")
        self._router.callback_query.register(self.handle_action_cancel, F.data == "action_cancel")

    @property
    def router(self) -> Router:
        return self._router

    async def start(self, message: Message):
        try:
            user = UserContext(
                id=message.from_user.id,
                name=message.from_user.first_name,
                lang=message.from_user.language_code
            )
        except Exception as e:
            logger.error(f"Failed to extract user info from message: {e}")
            return

        welcome_text = await self._service.start(user)
        keyboard = self._service.get_keyboard("main", user_name=user.name)
        await message.answer(welcome_text, parse_mode="HTML", reply_markup=keyboard)

    async def message_handler(self, message: Message):
        try:
            msg = MessageContext(
                msg_id=message.message_id,
                date=message.date,
                chat_id=message.chat.id,
                text=message.text or ""
            )
        except Exception as e:
            logger.error(f"Failed to extract message info: {e}")
            return

        answer_text = await self._service.echo_message(msg)
        await message.answer(answer_text, parse_mode="HTML")

    async def handle_main_menu(self, callback: CallbackQuery):
        """Обработка кнопки старт/главное меню"""
        await callback.answer()
        user = UserContext(
            id=callback.from_user.id,
            name=callback.from_user.first_name,
            lang=callback.from_user.language_code
        )
        welcome_text = await self._service.start(user)
        keyboard = self._service.get_keyboard("main", user_name=user.name)

        await callback.message.edit_text(welcome_text, parse_mode="HTML", reply_markup=keyboard)

    async def handle_settings_open(self, callback: CallbackQuery):
        """Открытие меню настроек"""
        await callback.answer()
        keyboard = self._service.get_keyboard("settings")
        settings_text = "⚙️ <b>Настройки бота</b>\nВыберите раздел:"

        # Проверяем, нужно ли редактировать сообщение
        if callback.message.text != settings_text or callback.message.reply_markup != keyboard:
            await callback.message.edit_text(settings_text, parse_mode="HTML", reply_markup=keyboard)

    async def handle_help(self, callback: CallbackQuery):
        """Обработка кнопки помощи"""
        await callback.answer()
        help_text = """
🤖 <b>Помощь по боту</b>

Доступные команды:
• /start - Начать работу
• Настройки - Настройки бота
• Помощь - Эта справка

Бот отвечает на любые сообщения эхом.
        """
        keyboard = self._service.get_keyboard("main")

        # Проверяем, нужно ли редактировать сообщение
        if callback.message.text != help_text or callback.message.reply_markup != keyboard:
            await callback.message.edit_text(help_text, parse_mode="HTML", reply_markup=keyboard)

    async def handle_settings_menu(self, callback: CallbackQuery):
        """Обработка пунктов меню настроек"""
        await callback.answer()
        setting_type = callback.data.split(":")[1]

        if setting_type == "notifications":
            text = "🔔 <b>Настройки уведомлений</b>\nЗдесь можно настроить уведомления"
        elif setting_type == "language":
            text = "🌐 <b>Настройки языка</b>\nВыберите язык интерфейса"
        elif setting_type == "security":
            text = "🔒 <b>Настройки безопасности</b>\nНастройки безопасности аккаунта"
        else:
            text = "⚙️ <b>Настройки</b>\nНеизвестный раздел"

        keyboard = self._service.get_keyboard("confirm")

        # Проверяем, нужно ли редактировать сообщение
        if callback.message.text != text or callback.message.reply_markup != keyboard:
            await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)

    async def handle_main_menu_back(self, callback: CallbackQuery):
        """Возврат в главное меню"""
        await self.handle_main_menu(callback)

    async def handle_action_confirm(self, callback: CallbackQuery):
        """Подтверждение действия"""
        await callback.answer("Действие подтверждено! ✅")
        await self.handle_main_menu(callback)

    async def handle_action_cancel(self, callback: CallbackQuery):
        """Отмена действия"""
        await callback.answer("Действие отменено! ❌")
        await self.handle_main_menu(callback)
