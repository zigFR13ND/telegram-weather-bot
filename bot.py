import os
import logging  # 📌 Логирование (показывает ошибки)
import requests  # 📌 Запросы к API
from aiogram import Bot, Dispatcher, types  # 📌 aiogram – библиотека для ботов
from aiogram.types import Message  # 📌 Тип сообщения
from aiogram.utils import executor  # 📌 Запуск бота
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
TGBOT_API_KEY = os.getenv('TGBOT_API_KEY')  # Получаем токен

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  # Получаем токен

logging.basicConfig(level=logging.INFO) # ✅ Включаем логирование (чтобы видеть ошибки)

bot = Bot(token=TGBOT_API_KEY) # ✅ Создаём объект бота
dp = Dispatcher(bot) # ✅ Создаём "диспетчер" (обработчик команд)

# ✅ Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

# ✅ Обрабатываем команду /weather
@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    await message.answer("Введите название города для прогноза:")

# ✅ Обрабатываем ввод города
@dp.message_handler()
async def get_weather(message: Message):
    city = message.text.strip()  # 📌 Получаем город, удаляем пробелы
    weather_today_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    weather_today_response = requests.get(weather_today_url)

    if weather_today_response.status_code == 200:
        weather_today = weather_today_response.json() # Преобразуем JSON в словарь.
        temp = weather_today["main"]["temp"] # Достаём температуру.
        if temp > 0:
            temp = f'+{temp}'
        wind = weather_today["wind"]["speed"] # Достаём скорость ветра.
        description = weather_today["weather"][0]["description"] # Достаём описание погоды.
        weather_today_text = (
            f"📍 Город: {city}\n"
            f"🌡 Температура: {temp}°C\n"
            f"💨 Ветер: {wind} м/с\n"
            f"🌤 Описание: {description}"
        )
    else:
        weather_today_text = "❌ Ошибка! Город не найден."

    await message.answer(weather_today_text)  # 📩 Отправляем ответ


# ✅ Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
