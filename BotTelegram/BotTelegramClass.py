import asyncio
import sys
import platform
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен вашего бота
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Создаем объект бота
bot = Bot(TOKEN)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("👋 Привет"), KeyboardButton("❓ Помощь")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я тестовый бот.",
        reply_markup=reply_markup
    )

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "👋 Привет":
        await update.message.reply_text("Привет! Как дела?")
    elif text == "❓ Помощь":
        await update.message.reply_text("Чем могу помочь?")
    else:
        await update.message.reply_text("Я вас не понимаю. Воспользуйтесь кнопками меню.")

# Обработчик других типов контента
async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправляйте только текстовые сообщения!")

def run_bot():
    # Настройка для Windows и Python 3.8
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.AUDIO, handle_other))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
