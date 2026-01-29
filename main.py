import asyncio
import bots
from core.registry import register_bot
from utils.config import config
from utils.logger import logger

async def main():
    await register_bot.init_all()
    await register_bot.start_all()

if __name__ == "__main__":
    asyncio.run(main())
