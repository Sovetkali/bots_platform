import asyncio
from utils.logger import logger

class BotRegistry:
    def __init__(self):
        self._factories = {}
        self._instances = {}

    def register(self, name: str, factory: callable):
        if name in self._factories:
            raise ValueError(f"Bot '{name}' already registered")

        self._factories[name] = factory
        logger.info(f"Bot registered: {name}")

    async def init_all(self):
        """
        Создаёт инстансы ботов через фабрики.
        """
        for name, factory in self._factories.items():
            logger.info(f"Initializing bot: {name}")

            try:
                bot = factory()
                self._instances[name] = bot
            except Exception:
                logger.exception(f"Failed to initialize bot: {name}")
                raise  # тут лучше падать сразу

    async def start_all(self):
        """
        Запускает всех ботов параллельно.
        """
        logger.info("Starting all bots...")

        tasks = []

        for name, bot in self._instances.items():
            logger.info(f"Starting bot: {name}")
            tasks.append(self._safe_start(name, bot))

        await asyncio.gather(*tasks)

        logger.info("All bots started")

    async def stop_all(self):
        logger.info("Stopping all bots...")
        tasks = [self._safe_stop(name, bot) for name, bot in self._instances.items()]
        await asyncio.gather(*tasks)
        logger.info("All bots stopped")

    async def _safe_start(self, name: str, bot):
        try:
            await bot.start()
        except Exception:
            logger.exception(f"Bot '{name}' failed to start")

    async def _safe_stop(self, name: str, bot):
        try:
            await bot.stop()
        except Exception:
            logger.exception(f"Bot '{name}' failed to stop")

register_bot = BotRegistry()
