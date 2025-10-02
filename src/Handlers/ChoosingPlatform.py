from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src.Handlers import globals
from src.Handlers.OrderDesc import order_description
from src.common import bot

def versions_kb():
    button1 = KeyboardButton(text="Enhanced")
    button2 = KeyboardButton(text="Legacy")

    versions_des.add(button1, button2)

versions_des = ReplyKeyboardMarkup(resize_keyboard=True)
versions_kb()

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
    globals.data_for_reg[message.chat.id]["password"] = message.text
    login = globals.data_for_reg[message.chat.id]["login"]
    password = globals.data_for_reg[message.chat.id]["password"]
    await bot.send_message(
        message.chat.id, f"Спасибо, ваши данные:\nЛогин: {login}\nПароль: {password}"
    )
    # Можно удалить данные, если больше не нужны:
    if not globals.is_changing_data:
        await bot.reply_to(
                message,
                "Выберете версию:",
                reply_markup=versions_des
            )
        globals.user_step[message.chat.id]["step"] = "version_of_game"
    else:
        globals.is_changing_data = False
        await globals.clicker.plat_clicker(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "version_of_game")
async def version_of_game(message):

    if message.chat.id not in globals.order_des or not isinstance(globals.order_des[message.chat.id], dict):
        globals.order_des[message.chat.id] = {}

    globals.order_des[message.chat.id]["version"] = message.text
    version = globals.order_des[message.chat.id]["version"]
    await bot.send_message(
        message.chat.id, f"Ваша версия игры: {version}"
    )

    globals.order_des[message.chat.id]["amount"] = 'не задано'
    globals.order_des[message.chat.id]["levels"] = 'не задано'
    globals.order_des[message.chat.id]["unlocks"] = 'не задано'

    await order_description(message)