import os
import logging  # 📌 Логирование (показывает ошибки)
import requests  # 📌 Запросы к API
from aiogram import Bot, Dispatcher, types  # 📌 aiogram – библиотека для ботов
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  # 📌 Тип сообщения, кнопки
from aiogram.utils import executor  # 📌 Запуск бота
from dotenv import load_dotenv # 📌 для работы с токеном в .env
from database import create_db, save_city, get_popular_cities # 📌 Импортируем базу данных

load_dotenv()  # Загружаем переменные из .env

# Получаем токен
TGBOT_API_KEY = os.getenv('TGBOT_API_KEY')  
# Получаем токен
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')  

# ✅ Включаем логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO) 

# ✅ Создаём объект бота
bot = Bot(token=TGBOT_API_KEY) 
# ✅ Создаём "диспетчер" (обработчик команд)
dp = Dispatcher(bot)

# ✅ Создаём базу данных при запуске
create_db() 

# ✅ Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

# ✅ Обрабатываем команду /weather (предлагаем популярные города)
@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    user_id = message.from_user.id  # 📌 ID пользователя
    popular_cities = get_popular_cities(user_id)  # 📌 Получаем популярные города
#    await message.answer("Введите название города для прогноза:")

    # 📌 Создаём кнопки
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in popular_cities:
        keyboard.add(KeyboardButton(city))  # ✅ Добавляем кнопку с городом

    await message.answer("Введите город или выберите из популярных:", reply_markup=keyboard)

# ✅ Обрабатываем ввод города
@dp.message_handler()
async def get_weather(message: Message):
    city = message.text.strip()  # 📌 Получаем город, удаляем пробелы
    user_id = message.from_user.id
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
        save_city(user_id, city)  # ✅ Сохраняем город в базу
    else:
        weather_today_text = "❌ Ошибка! Город не найден."

    await message.answer(weather_today_text)  # 📩 Отправляем ответ


# ✅ Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
