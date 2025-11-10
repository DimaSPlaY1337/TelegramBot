from src.Handlers.Telegram.ChoosingPlatform import choosing_platform
from src.common import bot
from src.dao.models import AsyncSessionLocal, User
from src.Handlers.Telegram.rules import error_handler
import traceback

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    """Приветствие и регистрация пользователя"""
    try:
        async with AsyncSessionLocal() as session:
            user = await session.get(User, message.from_user.id)

            if not user:
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                )
                session.add(user)
                await session.commit()
                await bot.reply_to(message, "Добро пожаловать! Вы зарегистрированы.")
            else:
                await bot.reply_to(message, "С возвращением!")

        # Начинаем процесс выбора платформы
        await choosing_platform(message)

    except Exception as e:
        print(f"Ошибка в send_welcome: {e}")
        print(traceback.format_exc())
        await error_handler(message.chat.id, traceback.format_exc())