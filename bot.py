import os
import logging  # 📌 Логирование (показывает ошибки)
import requests  # 📌 Запросы к API
from aiogram import Bot, Dispatcher, types  # 📌 aiogram – библиотека для ботов
from aiogram.types import Message  # 📌 Тип сообщения
from aiogram.utils import executor  # 📌 Запуск бота
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
TOKEN = os.getenv('TG_WEATHER_API_KEY')  # Получаем токен

logging.basicConfig(level=logging.INFO) # ✅ Включаем логирование (чтобы видеть ошибки)

bot = Bot(token=TOKEN) # ✅ Создаём объект бота
dp = Dispatcher(bot) # ✅ Создаём "диспетчер" (обработчик команд)

# ✅ Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

# ✅ Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
