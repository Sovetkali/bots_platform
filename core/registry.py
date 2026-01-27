from utils.logger import logger

class BotRegistry:
    def __init__(self):
        self._bots_classes = {}
        self._instances = {}

    def register(self, name: str, bot_class: type):
        self._bots_classes[name] = bot_class

    async def init_all(self):
        for name, bot_class in self._bots_classes.items():
            logger.info(f"Initializing bot: {name}")
            self._instances[name] = bot_class()

    async def start_all(self):
        for client in self._instances.values():
            logger.info(f"Starting bot: {client}")
            await client.start()

    async def stop_all(self):
        for client in self._instances.values():
            await client.stop()


register_bot = BotRegistry()
