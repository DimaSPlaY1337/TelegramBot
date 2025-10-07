#!/usr/bin/python
import asyncio
from src import Handlers # NoQa
from src.common import bot

if __name__ == '__main__':
    asyncio.run(bot.polling())
    # Метод polling, например
    # в aiogram или python - ботах, запускает непрерывный цикл опроса событий(например, новых сообщений от пользователей, команд и других апдейтов из внешнего API, например Telegram).