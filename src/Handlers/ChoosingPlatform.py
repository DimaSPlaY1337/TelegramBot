from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from src.Handlers import globals
from src.Handlers.OrderDesc import order_description
from src.common import bot

user_platforms = {}

def get_on_start_kb():
    button1 = KeyboardButton(text="Steam")
    button2 = KeyboardButton(text="EpicGames")
    button3 = KeyboardButton(text="Rockstar")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button1, button2, button3)
    return markup

async def choosing_platform(message):
    await bot.reply_to(
        message,
        "Какая платформа игры? (Steam, EpicGames, Rockstar)",
        reply_markup=get_on_start_kb()
    )


@bot.message_handler(func=lambda m: m.text in ["Steam", "EpicGames", "Rockstar"])
async def platform_choice(message):
    # сохраняем выбор в "переменную" (для каждого чата свой)
    globals.platform = message.text

    await bot.send_message(
        message.chat.id,
        f"Вы выбрали: {globals.platform}"
    )
    await order_description(message)