import os
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(os.environ['CheatingBot_TELEGRAM_TOKEN'])

platform = ""
user_step = {}
data_for_reg = {}
order_des = {}
app_list = []
type_of_soft = ""
clicker = None
is_changing_data = False