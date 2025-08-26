from src.Clikers.GTACliker import gta_cliker
from src.Clikers.RockstarCliker import rockstar_cliker
from src.Clikers.SteamCleaker import steam_cliker
from src.common import bot
from src.dao.models import AsyncSessionLocal, User


# text = "Hello"
# await bot.reply_to(message, text)
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
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
        # await choosing_platform(message)
        # await steam_cliker(message)
        # await rockstar_cliker(message)
        await gta_cliker(message)