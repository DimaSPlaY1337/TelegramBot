from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from src.Handlers import globals
from src.common import bot

order = []
markup_des = ReplyKeyboardMarkup(resize_keyboard=True)

def continue_kb():
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")

    markup_q = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_q.add(button1, button2)

    return markup_q

def choose_kb():
    button1 = KeyboardButton(text="Money")
    button2 = KeyboardButton(text="Levels")
    button3 = KeyboardButton(text="Items")

    markup_des.add(button1, button2, button3)

    return markup_des

async def order_description(message):
    await bot.reply_to(
        message,
        "Состав заказа (деньги, уровни и тд)",
        reply_markup=choose_kb()
    )

async def order_output(message):
    full_order = ""
    for item in order:  # for each
        full_order += item + ", "
    await bot.send_message(message.chat.id, f"Вы выбрали: {full_order[:-2]}")
    globals.order = full_order

@bot.message_handler(func=lambda m: m.text in ["Money", "Levels", "Items"])
async def order_choice(message):
    # сохраняем выбор в "переменную" (для каждого чата свой)
    if message.text not in order:
        order.append(message.text)

        if len(order) != len(markup_des.keyboard[0]):
            await bot.reply_to(
                message,
                "Что то еще?",
                reply_markup=continue_kb()
            )
        else:
            await order_output(message)
    else:
        await bot.send_message(message.chat.id, f"Вы это уже выбрали!\nВыберете что то другое.")
        await order_description(message)

@bot.message_handler(func=lambda m: m.text in ["Да", "Нет"])
async def order_continue(message):
    if message.text == "Да":
        await order_description(message)
    else:
        await order_output(message)
