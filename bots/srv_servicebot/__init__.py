from core.registry import register_bot
from core.bot_container import container
from utils.bots_config import BOT_CONFIGS

container.register_bot(BOT_CONFIGS['servicebot']['name'], BOT_CONFIGS['servicebot'])

def create_bot():
    return container.get_bot(BOT_CONFIGS['servicebot']['name'])

register_bot.register(BOT_CONFIGS['servicebot']['name'], create_bot)
