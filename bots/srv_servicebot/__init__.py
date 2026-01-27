from core.registry import register_bot
from .client import ServiceBotClient

register_bot.register(ServiceBotClient.name, ServiceBotClient)
