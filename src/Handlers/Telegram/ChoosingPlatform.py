from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from src.Handlers.Telegram.OrderDesc import order_description
import src.common as common
from src.common import bot
from src.Handlers.Telegram.rules import error_handler
import traceback

# Клавиатуры
versions_des = None


def versions_kb():
    """Клавиатура для выбора версии игры"""
    global versions_des
    button1 = KeyboardButton(text="enhanced")
    button2 = KeyboardButton(text="legacy")
    versions_des = ReplyKeyboardMarkup(resize_keyboard=True)
    versions_des.add(button1, button2)
    return versions_des


def get_on_start_kb():
    """Клавиатура для выбора платформы"""
    button1 = KeyboardButton(text="steam")
    button2 = KeyboardButton(text="epicgames")
    button3 = KeyboardButton(text="rockstar")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button1, button2, button3)
    return markup


async def choosing_platform(message):
    """Начало процесса выбора платформы"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.set_step("choose_platform")

        await bot.reply_to(
            message,
            "Какая платформа игры? (steam, epicgames, rockstar)",
            reply_markup=get_on_start_kb()
        )
    except Exception as e:
        print(f"Ошибка в choosing_platform: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id)


@bot.message_handler(
    func=lambda m: common.get_customer(m.chat.id).get_step() == "choose_platform"
                   and m.text in ["steam", "epicgames", "rockstar"]
)
async def platform_choice(message):
    """Обработка выбора платформы"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.platform = message.text

        await bot.send_message(
            chat_id,
            f"Вы выбрали: {customer.platform}",
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(chat_id, "Введите ваш логин:")

        customer.set_step("login")
    except Exception as e:
        print(f"Ошибка в platform_choice: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id)


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "login")
async def get_login(message):
    """Получение логина от пользователя"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.login = message.text
        customer.set_step("password")

        await bot.send_message(
            chat_id,
            "Введите ваш пароль:",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        print(f"Ошибка в get_login: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id)


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "password")
async def get_password(message):
    """Получение пароля и переход к выбору версии"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.password = message.text

        await bot.send_message(
            chat_id,
            f"Спасибо, ваши данные:\nЛогин: {customer.login}\nПароль: {customer.password}"
        )

        if not customer.is_changing_data:
            versions_kb()
            await bot.reply_to(
                message,
                "Выберете версию:",
                reply_markup=versions_des
            )
            customer.set_step("version_of_game")
        else:
            customer.is_changing_data = False
            if customer.clicker:
                await customer.clicker.plat_clicker(message)
    except Exception as e:
        print(f"Ошибка в get_password: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id)


@bot.message_handler(func=lambda m: common.get_customer(m.chat.id).get_step() == "version_of_game")
async def version_of_game(message):
    """Получение версии игры и переход к описанию заказа"""
    try:
        chat_id = message.chat.id
        customer = common.get_customer(chat_id)
        customer.order_des["version"] = message.text

        await bot.send_message(
            chat_id,
            f"Ваша версия игры: {customer.order_des['version']}"
        )

        # Инициализируем остальные поля заказа
        customer.order_des["amount"] = "не задано"
        customer.order_des["levels"] = "не задано"
        customer.order_des["unlocks"] = "не задано"

        await order_description(message)
    except Exception as e:
        print(f"Ошибка в version_of_game: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id)