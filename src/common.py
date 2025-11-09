import os
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(os.environ['CheatingBot_TELEGRAM_TOKEN'])

# Словарь для хранения объектов Customer по chat_id
customers: dict = {}

def get_customer(chat_id: int):
    """Получить или создать объект Customer для пользователя"""
    if chat_id not in customers:
        from src.Handlers.Telegram.Customer import Customer
        customers[chat_id] = Customer()
    return customers[chat_id]


def clear_customer(chat_id: int):
    """Удалить данные Customer для пользователя"""
    if chat_id in customers:
        del customers[chat_id]

platform = ""
user_step = {}
data_for_reg = {}
order_des = {}
app_list = []
type_of_soft = ""
clicker = None
is_changing_data = False