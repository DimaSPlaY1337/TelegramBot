from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from src.Handlers import globals
from src.common import bot

def choose_kb():
    button1 = KeyboardButton(text="Money")
    button2 = KeyboardButton(text="Levels")
    button3 = KeyboardButton(text="Items")

    markup_des.add(button1, button2, button3)

markup_des = ReplyKeyboardMarkup(resize_keyboard=True)
choose_kb()

def continue_kb():
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")

    markup_q = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_q.add(button1, button2)

    return markup_q



async def order_description(message):
    globals.user_step[message.chat.id] = {"step": "order_des"}
    await bot.reply_to(
        message,
        "Состав заказа (деньги, уровни и тд)",
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
        f"Items: {data.get('items', 'не задано')}"
    )

    await bot.send_message(chat_id, full_order)
    globals.order = full_order

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "order_des")
async def order_choice(message):
    chat_id = message.chat.id

    # Если для чата ещё нет записи в order_des — создаём
    if chat_id not in globals.order_des:
        globals.order_des[chat_id] = {}

    # Проверка: выбрано ли это уже
    if message.text == "Money" and "amount" not in globals.order_des[chat_id]:
        await bot.send_message(chat_id, "Введите сумму:", reply_markup=ReplyKeyboardRemove())
        globals.user_step[chat_id] = {"step": "money"}

    elif message.text == "Levels" and "levels" not in globals.order_des[chat_id]:
        await bot.send_message(chat_id, "Введите уровни:", reply_markup=ReplyKeyboardRemove())
        globals.user_step[chat_id] = {"step": "levels"}

    elif message.text == "Items" and "items" not in globals.order_des[chat_id]:
        await bot.send_message(chat_id, "Введите название предмета:", reply_markup=ReplyKeyboardRemove())
        globals.user_step[chat_id] = {"step": "items"}

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

@bot.message_handler(func=lambda m: globals.user_step.get(m.chat.id, {}).get("step") == "items")
async def get_items(message):
    globals.order_des[message.chat.id]["items"] = message.text
    await order_question(message)

async def order_question(message):
    if len(globals.order_des[message.chat.id]) != len(markup_des.keyboard[0]):
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
