# import src.common as common
# from src.Handlers.Digiseller.IO_utils import *
# from src.common import *
#
# async def choosing_platform(dialog_id):
#     await send_message(token, dialog_id, "Какая платформа игры? (Steam, EpicGames, Rockstar)")
#     common.user_step[dialog_id] = {"step": "choose_platform"}
#
# async def platform_choice(dialog_id):
#     messages = get_messages(token, dialog_id)
#
#     await bot.send_message(message.chat.id, f"Вы выбрали: {common.platform}", reply_markup=ReplyKeyboardRemove())
#     await bot.send_message(message.chat.id, "Введите ваш логин:")
#
#     # Меняем шаг на "ожидание логина"
#     common.user_step[message.chat.id] = {"step": "login"}
#     common.data_for_reg[message.chat.id] = {"login": ""}
from IO_utils import *
from OrderDesc import order_description
from src.Clikers.Digiseller.SteamClicker import SteamClicker


async def choosing_platform(token, dialog_id, message_data, customer):
    # platform_text = (
    #     "Какая платформа игры?\n"
    #     "Напишите одну из следующих:\n"
    #     "- Steam\n"
    #     "- EpicGames\n"
    #     "- Rockstar"
    # )
    # await send_message(token, dialog_id, platform_text)
    # customer.user_step = "choose_platform"

    customer.platform = "steam"
    customer.data_for_reg["login"] = "mustypalate7710"
    customer.data_for_reg["password"] = "kFzrZYF_JcJF3r"
    customer.order_des = {
        "version": "enhanced",
        "amount": 20000000,
        "levels": 120,
        "unlocks": "Standard Unlocks"
    }
    customer.clicker = SteamClicker()
    await customer.clicker.plat_clicker(token, dialog_id, message_data, customer)


async def handle_platform_choice(token, dialog_id, message_text, customer):
    if message_text in ["steam", "epicgames", "rockstar"]:
        customer.platform = message_text

        platform_confirm = f"Вы выбрали: {customer.platform}"
        await send_message(token, dialog_id, platform_confirm)

        login_request = "Введите ваш логин:"
        await send_message(token, dialog_id, login_request)

        customer.user_step = "login"
        customer.data_for_reg = {"login": "", "password": ""}
    else:
        await send_message(token, dialog_id, "Пожалуйста, выберите одну из платформ: Steam, EpicGames или Rockstar")


async def handle_login(token, dialog_id, message_text, customer):
    customer.data_for_reg["login"] = message_text
    customer.user_step = "password"

    password_request = "Введите ваш пароль:"
    await send_message(token, dialog_id, password_request)


async def handle_password(token, dialog_id, message_text, customer):
    customer.data_for_reg["password"] = message_text

    login = customer.data_for_reg["login"]
    password = customer.data_for_reg["password"]

    credentials_confirm = f"Спасибо, ваши данные:\nЛогин: {login}\nПароль: {password}"
    await send_message(token, dialog_id, credentials_confirm)

    if not customer.is_changing_data:
        version_request = (
            "Выберите версию игры:\n"
            "- Enhanced\n"
            "- Legacy"
        )
        await send_message(token, dialog_id, version_request)
        customer.user_step = "version_of_game"
    elif customer.is_changing_data:
        await customer.clicker.plat_clicker(token, dialog_id, message_text, customer)


async def handle_version(token, dialog_id, message_text, customer):
    if message_text in ["enhanced", "legacy"]:
        customer.order_des = {
            "version": message_text,
            "amount": "не задано",
            "levels": "не задано",
            "unlocks": "не задано"
        }

        version_confirm = f"Ваша версия игры: {message_text}"
        await send_message(token, dialog_id, version_confirm)

        await order_description(token, dialog_id, customer)
    else:
        await send_message(token, dialog_id, "Пожалуйста, выберите Enhanced или Legacy")
