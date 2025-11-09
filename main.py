#!/usr/bin/python

import asyncio
import logging
from src import Handlers  # NoQa
from src.common import bot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    try:
        logger.info("Бот запущен и начинает опрос Telegram API")
        await bot.polling()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(main())