import asyncio
import os

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(os.environ['CheatingBot_TELEGRAM_TOKEN'])

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am EchoBot. \n Write something I will repeat'
    await bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

if __name__ == '__main__':
    asyncio.run(bot.polling())