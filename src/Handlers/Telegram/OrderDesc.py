from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from src.Clikers.Telegram.RockstarClicker import RockstarClicker
from src.Clikers.Telegram.SteamClicker import SteamClicker
from src.Clikers.Telegram.EpicgamesClicker import EpicgamesClicker
import src.common as common
from src.common import bot
from src.Handlers.Telegram.rules import error_handler
import traceback

# Клавиатуры
unlocks_des = None
markup_des = None


def unlocks_kb():
    """Клавиатура для выбора типа разблокировок"""
    global unlocks_des
    button1 = KeyboardButton(text="standard unlocks")
    button2 = KeyboardButton(text="super unlocks")
    unlocks_des = ReplyKeyboardMarkup(resize_keyboard=True)
    unlocks_des.add(button1, button2)
    return unlocks_des


def choose_kb():
    """Клавиатура для выбора позиций в заказе"""
    global markup_des
    button1 = KeyboardButton(text="money")
    button2 = KeyboardButton(text="levels")
    button3 = KeyboardButton(text="unlocks")
    markup_des = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_des.add(button1, button2, button3)
    return markup_des


def continue_kb():
    """Клавиатура для продолжения заказа"""
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")
    markup_q = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_q.add(button1, button2)
    return markup_q


async def order_description(message):
    """Начало процесса описания заказа"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.set_step("order_des")

        choose_kb()
        await bot.reply_to(
            message,
            "Какие позиции вы хотели бы видеть в вашем заказе?",
            reply_markup=markup_des
        )
    except Exception as e:
        print(f"Ошибка в order_description: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


async def order_output(message):
    """Вывод финального заказа и выбор кликкера"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        await bot.send_message(
            chat_id,
            customer.get_order_summary(),
            reply_markup=ReplyKeyboardRemove()
        )

        # Создаем кликкер в зависимости от платформы
        if customer.platform == "steam":
            customer.clicker = SteamClicker()
        elif customer.platform == "epicgames":
            customer.clicker = EpicgamesClicker()
        elif customer.platform == "rockstar":
            customer.clicker = RockstarClicker()

        if customer.clicker:
            await customer.clicker.plat_clicker(message)
    except Exception as e:
        print(f"Ошибка в order_output: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "order_des")
async def order_choice(message):
    """Обработка выбора позиции в заказе"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if message.text == "money" and customer.order_des["amount"] == "не задано":
            await bot.send_message(chat_id, "Введите сумму:", reply_markup=ReplyKeyboardRemove())
            customer.set_step("money")
        elif message.text == "levels" and customer.order_des["levels"] == "не задано":
            await bot.send_message(chat_id, "Введите уровни:", reply_markup=ReplyKeyboardRemove())
            customer.set_step("levels")
        elif message.text == "unlocks" and customer.order_des["unlocks"] == "не задано":
            unlocks_kb()
            await bot.reply_to(
                message,
                "Выберете тип unlocks:",
                reply_markup=unlocks_des
            )
            customer.set_step("unlocks")
        else:
            await bot.send_message(chat_id, "Вы это уже выбрали!\nВыберите что-то другое.")
            await order_description(message)
    except Exception as e:
        print(f"Ошибка в order_choice: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "money")
async def get_money(message):
    """Получение суммы денег"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.order_des["amount"] = message.text
        await order_question(message)
    except Exception as e:
        print(f"Ошибка в get_money: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "levels")
async def get_levels(message):
    """Получение уровней"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.order_des["levels"] = message.text
        await order_question(message)
    except Exception as e:
        print(f"Ошибка в get_levels: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "unlocks")
async def get_items(message):
    """Получение типа разблокировок"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.order_des["unlocks"] = message.text
        await order_question(message)
    except Exception as e:
        print(f"Ошибка в get_items: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


async def order_question(message):
    """Вопрос о дополнительных позициях в заказе"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)

        if (customer.order_des["levels"] == "не задано"
                or customer.order_des["unlocks"] == "не задано"
                or customer.order_des["amount"] == "не задано"):

            await bot.reply_to(
                message,
                "Что то еще?",
                reply_markup=continue_kb()
            )
            customer.set_step("order_con")
        else:
            await order_output(message)
    except Exception as e:
        print(f"Ошибка в order_question: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "order_con")
async def order_continue(message):
    """Обработка ответа о продолжении заказа"""
    try:
        if message.text == "Да":
            await order_description(message)
        else:
            await order_output(message)
    except Exception as e:
        print(f"Ошибка в order_continue: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())