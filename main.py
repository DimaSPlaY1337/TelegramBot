import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from src import Handlers #NoQa

bot = AsyncTeleBot(os.environ['CheatingBot_TELEGRAM_TOKEN'])

if __name__ == '__main__':
    asyncio.run(bot.polling())