from bots.srv_servicebot.service import ServiceBotService
from bots.srv_servicebot.router import ServiceBotRouter
from bots.srv_servicebot.client import ServiceBotClient

BOT_CONFIGS = {
    'servicebot': {
        'name': 'servicebot',
        'service_class': ServiceBotService,
        'router_class': ServiceBotRouter,
        'client_class': ServiceBotClient,
        'dependencies': {}  # Можно передать дополнительные зависимости
    }
}
