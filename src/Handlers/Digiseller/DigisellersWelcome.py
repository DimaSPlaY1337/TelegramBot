from IO_utils import *

# Словарь для хранения данных пользователей по dialog_id
customers = {}

async def send_welcome(token, dialog_id, message_data):
    from Customer import Customer

    # Создаем или получаем клиента
    if dialog_id not in customers:
        customers[dialog_id] = Customer()

    customer = customers[dialog_id]

    # Регистрируем пользователя (аналогично Telegram боту)
    # welcome_text = "Добро пожаловать! Вы зарегистрированы."
    # await send_message(token, dialog_id, welcome_text)

    # Переходим к выбору платформы
    # await choosing_platform(token, dialog_id, message_data, customer)
