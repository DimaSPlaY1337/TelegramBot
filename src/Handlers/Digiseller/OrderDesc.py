from src.Clikers.Digiseller.EpicgamesClicker import EpicgamesClicker
from src.Clikers.Digiseller.RockstarClicker import RockstarClicker
from src.Clikers.Digiseller.SteamClicker import SteamClicker
from src.Handlers.Digiseller.IO_utils import *

async def order_description(token, dialog_id, customer):
    order_text = (
        "Какие позиции вы хотели бы видеть в вашем заказе?\n"
        "Напишите одну из следующих:\n"
        "- Money\n"
        "- Levels\n"
        "- Unlocks"
    )
    await send_message(token, dialog_id, order_text)
    customer.user_step = "order_des"


async def handle_order_choice(token, dialog_id, message_text, customer):
    if message_text == "money" and customer.order_des["amount"] == "не задано":
        await send_message(token, dialog_id, "Введите сумму:")
        customer.user_step = "money"
    elif message_text == "levels" and customer.order_des["levels"] == "не задано":
        await send_message(token, dialog_id, "Введите уровни:")
        customer.user_step = "levels"
    elif message_text == "unlocks" and customer.order_des["unlocks"] == "не задано":
        unlocks_text = (
            "Выберите тип Unlocks:\n"
            "- Standard Unlocks\n"
            "- Super Unlocks"
        )
        await send_message(token, dialog_id, unlocks_text)
        customer.user_step = "unlocks"
    else:
        await send_message(token, dialog_id, "Вы это уже выбрали!\nВыберите что-то другое.")
        await order_description(token, dialog_id, customer)


async def handle_money_input(token, dialog_id, message_text, customer):
    customer.order_des["amount"] = message_text
    await check_order_completion(token, dialog_id, message_text, customer)


async def handle_levels_input(token, dialog_id, message_text, customer):
    customer.order_des["levels"] = message_text
    await check_order_completion(token, dialog_id, message_text, customer)


async def handle_unlocks_input(token, dialog_id, message_text, customer):
    if message_text in ["Standard Unlocks", "Super Unlocks"]:
        customer.order_des["unlocks"] = message_text
        await check_order_completion(token, dialog_id, message_text, customer)
    else:
        await send_message(token, dialog_id, "Выберите Standard Unlocks или Super Unlocks")


async def check_order_completion(token, dialog_id, message_text, customer):
    if (customer.order_des["levels"] == 'не задано'
            or customer.order_des["unlocks"] == 'не задано'
            or customer.order_des["amount"] == 'не задано'):

        continue_text = (
            "Что-то еще?\n"
            "Напишите:\n"
            "- Да\n"
            "- Нет"
        )
        await send_message(token, dialog_id, continue_text)
        customer.user_step = "order_con"
    else:
        await order_output(token, dialog_id, message_text, customer)


async def handle_order_continue(token, dialog_id, message_text, customer):
    if message_text.lower() == "да":
        await order_description(token, dialog_id, customer)
    elif message_text.lower() == "нет":
        await order_output(token, dialog_id, message_text, customer)


async def order_output(token, dialog_id, message_text, customer):
    full_order = "Вы выбрали:\n"
    for key, value in customer.order_des.items():
        full_order += f"{key}: {value}\n"

    await send_message(token, dialog_id, full_order)

    # Здесь можно добавить запуск соответствующего клика (аналогично Telegram боту)
    completion_text = "Заказ принят! Ожидайте выполнения."
    await send_message(token, dialog_id, completion_text)

    if customer.platform == "steam":
        customer.clicker = SteamClicker()
    elif customer.platform == "epicgames":
        customer.clicker = EpicgamesClicker()
    elif customer.platform == "rockstar":
        customer.clicker = RockstarClicker()

    await customer.clicker.plat_clicker(token, dialog_id, message_text, customer)
