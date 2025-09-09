from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src.Handlers import globals
from src.common import bot

def unlocks_kb():
    button1 = KeyboardButton(text="Standard Unlocks")
    button2 = KeyboardButton(text="Super Unlocks")

    unlocks_des.add(button1, button2)

unlocks_des = ReplyKeyboardMarkup(resize_keyboard=True)
unlocks_kb()

def choose_kb():
    button1 = KeyboardButton(text="Money")
    button2 = KeyboardButton(text="Levels")
    button3 = KeyboardButton(text="Unlocks")

    markup_des.add(button1, button2, button3)

markup_des = ReplyKeyboardMarkup(resize_keyboard=True)
choose_kb()

def continue_kb():
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")

    markup_q = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_q.add(button1, button2)

    return markup_q


@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "order_choice")
async def order_description(message):
    globals.user_step[message.chat.id] = {"step": "order_des"}

    if message.chat.id not in globals.order_des or not isinstance(globals.order_des[message.chat.id], dict):
        globals.order_des[message.chat.id] = {}

    globals.order_des[message.chat.id]["amount"] = 'не задано'
    globals.order_des[message.chat.id]["levels"] = 'не задано'
    globals.order_des[message.chat.id]["unlocks"] = 'не задано'

    await bot.reply_to(
        message,
        "Какие позиции вы хотели бы видеть в вашем заказе?",
        reply_markup=markup_des
    )

async def order_output(message):
    chat_id = message.chat.id
    data = globals.order_des.get(chat_id, {})

    # Формируем текст только для этого пользователя
    full_order = (
        f"Вы выбрали: \n"
        f"Money: {data.get('amount', 'не задано')}\n"
        f"Levels: {data.get('levels', 'не задано')}\n"
        f"Unlocks: {data.get('unlocks', 'не задано')}"
    )

    await bot.send_message(chat_id, full_order, reply_markup=ReplyKeyboardRemove())
    globals.order = full_order

    if globals.platform == "EpicGames":
        from src.Clikers import epic_cliker
        await epic_cliker(message)
    elif globals.platform == "Rockstar":
        from src.Clikers import rockstar_cliker
        await rockstar_cliker(message)
    elif globals.platform == "Steam":
        from src.Clikers import steam_cliker
        await steam_cliker(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "order_des")
async def order_choice(message):
    chat_id = message.chat.id

    # Проверка: выбрано ли это уже
    if message.text == "Money" and globals.order_des[chat_id]["amount"] != 0:
        await bot.send_message(chat_id, "Введите сумму:", reply_markup=ReplyKeyboardRemove())
        globals.user_step[chat_id] = {"step": "money"}

    elif message.text == "Levels" and globals.order_des[chat_id]["levels"] != 0:
        await bot.send_message(chat_id, "Введите уровни:", reply_markup=ReplyKeyboardRemove())
        globals.user_step[chat_id] = {"step": "levels"}

    elif message.text == "Items" and globals.order_des[chat_id]["unlocks"] != 0:
        await bot.reply_to(
            message,
            "Выберете тип Unlocks:",
            reply_markup=unlocks_des
        )
        globals.user_step[chat_id] = {"step": "unlocks"}

    else:
        await bot.send_message(chat_id, "Вы это уже выбрали!\nВыберите что-то другое.")
        await order_description(message)

# --- Обработчики шагов ---
@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "money")
async def get_money(message):
    globals.order_des[message.chat.id]["amount"] = message.text
    await order_question(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "levels")
async def get_levels(message):
    globals.order_des[message.chat.id]["levels"] = message.text
    await order_question(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "unlocks")
async def get_items(message):
    globals.order_des[message.chat.id]["unlocks"] = message.text
    await order_question(message)

async def order_question(message):
    if (globals.order_des[message.chat.id]["levels"] == 'не задано'
            or globals.order_des[message.chat.id]["unlocks"] == 'не задано'
            or globals.order_des[message.chat.id]["levels"] == 'не задано'):
        await bot.reply_to(
            message,
            "Что то еще?",
            reply_markup=continue_kb()
        )
        globals.user_step[message.chat.id] = {"step": "order_con"}
    else:
        await order_output(message)

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "order_con")
async def order_continue(message):
    if message.text == "Да":
        await order_description(message)
    else:
        await order_output(message)
