import asyncio
import sys
import platform
import os
import random
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен вашего бота
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Создаем объект бота
bot = Bot(TOKEN)

# Возможные выборы для игры
choices = ["Камень", "Ножницы", "Бумага"]

# Функция для загрузки шуток из файла
def load_jokes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]  # Очищаем от лишних символов

# Получаем путь к текущей директории, где находится скрипт
current_directory = os.path.dirname(os.path.abspath(__file__))
# Строим полный путь к файлу 'jokes.txt'
file_path = os.path.join(current_directory, 'jokes.txt')

# Список айтишных шуток, теперь загружаемых из файла
it_jokes = load_jokes(file_path)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("👋 Привет"), KeyboardButton("❓ Помощь")],
        [KeyboardButton("🎮 Играть в Камень-Ножницы-Бумага"), KeyboardButton("🃏 Шутки")],
        [KeyboardButton("🎮 Запустить Dota 2")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Приветственное сообщение
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я проснулась!",
        reply_markup=reply_markup
    )

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "👋 Привет":
        keyboard = [
            [InlineKeyboardButton("Все хорошо", callback_data='good')],
            [InlineKeyboardButton("Плохо", callback_data='bad')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Привет! Как дела?", reply_markup=reply_markup)
    
    elif text == "❓ Помощь":
        await update.message.reply_text("Чем могу помочь?")

    elif text == "🎮 Играть в Камень-Ножницы-Бумага":
        keyboard = [[KeyboardButton(choice) for choice in choices]]
        keyboard.append([KeyboardButton("🔙 Вернуться в меню")])  # Добавляем кнопку "Вернуться в меню"
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

        await update.message.reply_text(
            "Выберите: Камень, Ножницы или Бумага:",
            reply_markup=reply_markup
        )

    elif text == "🃏 Шутки":
        joke = random.choice(it_jokes)  # Выбираем случайный анекдот
        await update.message.reply_text(joke)

    elif text in choices:
        user_choice = text
        bot_choice = random.choice(choices)

        if user_choice == bot_choice:
            result = "Ничья!"
        elif (user_choice == "Камень" and bot_choice == "Ножницы") or \
             (user_choice == "Ножницы" and bot_choice == "Бумага") or \
             (user_choice == "Бумага" and bot_choice == "Камень"):
            result = "Вы победили! 🎉"
        else:
            result = "Вы проиграли. 😢"

        keyboard = [[KeyboardButton(choice) for choice in choices]]
        keyboard.append([KeyboardButton("🔙 Вернуться в меню")])  # Добавляем кнопку "Вернуться в меню"
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

        await update.message.reply_text(
            f"Вы выбрали: {user_choice}\nБот выбрал: {bot_choice}\n{result}",
            reply_markup=reply_markup
        )

    elif text == "🔙 Вернуться в меню":
        keyboard = [
            [KeyboardButton("👋 Привет"), KeyboardButton("❓ Помощь")],
            [KeyboardButton("🎮 Играть в Камень-Ножницы-Бумага"), KeyboardButton("🃏 Шутки")],
            [KeyboardButton("🎮 Запустить Dota 2")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            f"Вы вернулись в главное меню, {update.effective_user.first_name}!",
            reply_markup=reply_markup
        )

    elif text == "🎮 Запустить Dota 2":
        try:
            # Укажите путь к Steam и ID игры Dota 2
            subprocess.Popen(r'Z:\SteamLibrary\steamapps\common\dota 2 beta\game\bin\win64\dota2.exe')
            await update.message.reply_text("Dota 2 запущена! 🎮")
        except Exception as e:
            await update.message.reply_text(f"Ошибка при запуске Dota 2: {e}")

    else:
        await update.message.reply_text("Я вас не понимаю. Воспользуйтесь кнопками меню.")

# Обработчик для инлайн кнопок (например, "Все хорошо" и "Плохо")
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Отправить ответ на клик (иначе кнопка не будет работать)

    if query.data == 'good':
        await query.edit_message_text("Рада это слышать! 😊")
    elif query.data == 'bad':
        await query.edit_message_text("Ой, надеюсь, скоро всё наладится! 😔")

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
    app.add_handler(CallbackQueryHandler(handle_callback))  # Добавляем обработчик для инлайн кнопок

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
