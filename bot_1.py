import os
import logging  # 📌 Логирование (показывает ошибки)
import requests  # 📌 Запросы к API
import aiohttp  # ✅ Асинхронные запросы
from aiogram import Bot, Dispatcher, types  # 📌 aiogram – библиотека для ботов
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove # 📌 Тип сообщения, кнопки
from aiogram.utils import executor  # 📌 Запуск бота
from dotenv import load_dotenv # 📌 для работы с токеном в .env
from database import create_db, save_city, get_popular_cities, show_user_cities # 📌 Импортируем базу данных

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

### ✅ **Функция для получения погоды (асинхронный запрос)**
async def get_weather(city):
    weather_today_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(weather_today_url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["main"]["temp"]
                    if temp > 0:
                        temp = f'+{temp}'
                    wind = data["wind"]["speed"]
                    description = data["weather"][0]["description"]

                    return (
                        f"📍 Город: {city}\n"
                        f"🌡 Температура: {temp}°C\n"
                        f"💨 Ветер: {wind} м/с\n"
                        f"🌤 Описание: {description.capitalize()}"
                    )
                elif response.status == 404:
                    return "❌ Ошибка! Город не найден."
                else:
                    return "⚠ Ошибка! Погодный сервер недоступен."

    except aiohttp.ClientError as e:
        logging.error(f"Ошибка API OpenWeather: {e.status} {e.message}")
        return f"❌ Ошибка! Погодный сервер вернул ошибку {e.status}."
    except aiohttp.ClientError as e:
        logging.error(f"Ошибка сети при запросе к OpenWeather: {e}")
        return "❌ Ошибка! Не удалось соединиться с сервером погоды."

# ✅ Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

# ✅ Обрабатываем команду /weather (предлагаем популярные города)
@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    user_id = message.from_user.id  # 📌 ID пользователя
    popular_cities = get_popular_cities(user_id)  # 📌 Получаем популярные города

    # 📌 Создаём кнопки
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if popular_cities:
        for city in popular_cities:
            keyboard.add(KeyboardButton(city))  # ✅ Добавляем кнопку с городом
        await message.answer("Введите город или выберите из популярных:", reply_markup=keyboard)
    else:
        await message.answer("Введите название города для прогноза:")  # ❌ Если городов нет – без кнопок

### ✅ **Обрабатываем ввод города (асинхронный запрос погоды)**
@dp.message_handler(lambda message: message.text)
async def process_city(message: Message):
    city = message.text.strip()  # 📌 Получаем город, удаляем пробелы
    user_id = message.from_user.id

    weather_info = await get_weather(city)  # ✅ Асинхронный вызов

    if "Ошибка" not in weather_info:
        save_city(user_id, city)  # ✅ Сохраняем город в базу

    await message.answer(weather_info, reply_markup=ReplyKeyboardRemove())# ✅ Отправляем сообщение и убираем кнопки

# ✅ Обрабатываем команду /history
@dp.message_handler(commands=["history"])
async def history_command(message: Message):
    user_id = message.from_user.id  # 📌 ID пользователя
    history = show_user_cities(user_id)  # 📌 Получаем список городов
    if not history:
        await message.answer("❌ История пуста. Используйте /weather, чтобы добавить города.")
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    for city in history.split("\n"):
        keyboard.add(KeyboardButton(city))

    await message.answer("📜 Ваши сохранённые города:", reply_markup=keyboard)


# ✅ Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
