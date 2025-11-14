from src.common import bot
import src.common as common
import traceback
import subprocess

async def error_handler(chat_id: int, error: str):
    """Обработчик ошибок - уведомляет пользователя и очищает данные"""
    try:
        await bot.send_message(
            chat_id,
            f"😕 Я упал в ошибку, нажмите /restart \n Сообщение ошибки: {error}"
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
        await error_handler(message.chat.id, traceback.format_exc())


@bot.message_handler(commands=['restart'])
async def restart_handler(message):
    """Команда для перезагрузки состояния бота"""
    try:
        processes = [
            "Sunrise.exe"
            "Launcher.exe",
            "LauncherPatcher.exe",
            "RockstarErrorHandler.exe",
            "RockstarService.exe",
            "SocialClubHelper.exe",
            "steam.exe",
            "steamservice.exe",
            "steamwebhelper.exe"
        ]

        for process in processes:
            subprocess.run(f"taskkill /IM {process} /F", shell=True)
        chat_id = message.chat.id
        common.clear_customer(chat_id)
        await bot.send_message(chat_id, "✅ Бот перезагружен. Введите /start для начала")
    except Exception as e:
        print(f"Ошибка при перезагрузке: {e}")
        await error_handler(message.chat.id, traceback.format_exc())