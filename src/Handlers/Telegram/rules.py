from src.common import bot
import src.common as common
import traceback

async def error_handler(chat_id: int):
    """Обработчик ошибок - уведомляет пользователя и очищает данные"""
    try:
        await bot.send_message(
            chat_id,
            "😕 Я упал в ошибку, нажмите /restart"
        )
    except Exception as e:
        print(f"Ошибка при отправке сообщения об ошибке: {e}")
    finally:
        # Очищаем данные пользователя
        common.clear_customer(chat_id)


async def wrap_handler(handler_func, message):
    """Обертка для защиты обработчиков от ошибок"""
    try:
        await handler_func(message)
    except Exception as e:
        print(f"Ошибка в обработчике: {e}")
        print(f"Трассировка: {traceback.format_exc()}")
        await error_handler(message.chat.id)


@bot.message_handler(commands=['restart'])
async def restart_handler(message):
    """Команда для перезагрузки состояния бота"""
    try:
        chat_id = message.chat.id
        common.clear_customer(chat_id)
        await bot.send_message(chat_id, "✅ Бот перезагружен. Введите /start для начала")
    except Exception as e:
        print(f"Ошибка при перезагрузке: {e}")
        await error_handler(message.chat.id)