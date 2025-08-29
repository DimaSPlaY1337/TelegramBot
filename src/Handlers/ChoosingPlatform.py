from sqlalchemy import false
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src.Clikers import *
from src.Handlers import globals
from src.Handlers.OrderDesc import order_description
from src.common import bot

is_changing_data = False

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
    globals.user_step[message.chat.id] = {"step": "choose_platform"}


@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "choose_platform" and m.text in ["Steam", "EpicGames", "Rockstar"])
async def platform_choice(message):
    globals.platform = message.text

    await bot.send_message(message.chat.id, f"Вы выбрали: {globals.platform}", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, "Введите ваш логин:")

    # Меняем шаг на "ожидание логина"
    globals.user_step[message.chat.id] = {"step": "login"}
    globals.data_for_reg[message.chat.id] = {"login": ""}


@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "login")
async def get_login(message):
    globals.data_for_reg[message.chat.id]["login"] = message.text
    globals.user_step[message.chat.id]["step"] = "password"
    await bot.send_message(
        message.chat.id, "Введите ваш пароль:", reply_markup=ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "password")
async def get_password(message):
    global is_changing_data
    globals.data_for_reg[message.chat.id]["password"] = message.text
    login = globals.data_for_reg[message.chat.id]["login"]
    password = globals.data_for_reg[message.chat.id]["password"]
    await bot.send_message(
        message.chat.id, f"Спасибо, ваши данные:\nЛогин: {login}\nПароль: {password}"
    )
    # Можно удалить данные, если больше не нужны:
    if not is_changing_data:
        await order_description(message)
    elif globals.platform == "EpicGames":
        from src.Clikers import epic_cliker
        is_changing_data = False
        await epic_cliker(message)
    elif globals.platform == "Rockstar":
        from src.Clikers import rockstar_cliker
        is_changing_data = False
        await rockstar_cliker(message)
    elif globals.platform == "Steam":
        from src.Clikers import steam_cliker
        is_changing_data = False
        await steam_cliker(message)


async def change_pass_and_login(message):
    global is_changing_data
    is_changing_data = True
    globals.user_step[message.chat.id] = {"step": "login"}
    await bot.send_message(message.chat.id, "Введите ваш логин:")