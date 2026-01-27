import asyncio
from utils.config import config
from utils.logger import logger
import bots.srv_servicebot
from core.registry import register_bot

async def main():
    logger.info(f"Starting service bot. DEV_MODE={config.DEV_MODE}")
    register_bot.init_all()
    await register_bot.start_all()

if __name__ == "__main__":
    asyncio.run(main())
