# Важно: сначала импортируем rules (содержит restart и error_handler)
from src.Handlers.Telegram import rules

# Затем импортируем Welcome (содержит /start и /help)
from src.Handlers.Telegram import Welcome

# Потом остальные обработчики
from src.Handlers.Telegram import ChoosingPlatform
from src.Handlers.Telegram import OrderDesc

