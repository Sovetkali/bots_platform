import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import bots
from core.registry import register_bot
from utils.logger import logger

async def startup():
    logger.info("Initializing and starting bots...")
    await register_bot.init_all()
    await register_bot.start_all()
    logger.info("Bots started.")

async def shutdown():
    logger.info("Stopping bots...")
    await register_bot.stop_all()
    logger.info("Bots stopped.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()

    yield

    await shutdown()

app = FastAPI(
    lifespan=lifespan
)

# run python main.py for development

async def main():
    await startup()

if __name__ == "__main__":
    asyncio.run(main())
