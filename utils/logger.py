import asyncio
import sys

from aiogram import Bot
from loguru import logger
from .config import config
from .logging_config import log_config

log_config.LOGS_DIR.mkdir(exist_ok=True)
logger.remove()

if log_config.ENV == True:
    logger.add(
        sys.stdout,
        level="DEBUG",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].no < 40
    )
    logger.add(
        sys.stderr,
        level="ERROR",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].no >= 40
    )
else:
    logger.add(
        log_config.LOGS_DIR / "debug.log",
        level="DEBUG",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].no < 40
    )
