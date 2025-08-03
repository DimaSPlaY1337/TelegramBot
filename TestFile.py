from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# Состояния (этапы диалога)
PLATFORM, CREDENTIALS, ORDER, TFA = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Какая платформа игры? (стим, эпик, Рокстар)")
    return PLATFORM

async def platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['platform'] = update.message.text
    await update.message.reply_text("Введите логин и пароль (через пробел):")
    return CREDENTIALS

async def credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    login_password = update.message.text.split()
    context.user_data['login'] = login_password[0]
    context.user_data['password'] = login_password[1] if len(login_password) > 1 else ''
    await update.message.reply_text("Состав заказа (например — деньги, уровни и т.д.):")
    return ORDER

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order'] = update.message.text
    # Если нужен 2FA:
    await update.message.reply_text("Если требуется код 2ФА, введите его. Если нет — напишите 'нет'.")
    return TFA

async def tfa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tfa_code = update.message.text
    context.user_data['tfa'] = tfa_code if tfa_code.lower() != 'нет' else None
    # Здесь все данные сохранены:
    await update.message.reply_text(f"Получено:\nПлатформа: {context.user_data['platform']}\nЛогин: {context.user_data['login']}\nПароль: {context.user_data['password']}\nЗаказ: {context.user_data['order']}\n2ФА: {context.user_data['tfa']}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Процесс отменён.")
    return ConversationHandler.END

app = ApplicationBuilder().token('ВАШ_ТОКЕН').build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, platform)],
        CREDENTIALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, credentials)],
        ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
        TFA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tfa)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

app.add_handler(conv_handler)
app.run_polling()
