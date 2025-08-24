#!/usr/bin/python
import asyncio
from src import Handlers # NoQa
from src.common import bot
#pip install -r .\requirements.txt

if __name__ == '__main__':
    asyncio.run(bot.polling())