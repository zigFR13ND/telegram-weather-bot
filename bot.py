import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import executor
from config import TGBOT_API_KEY
from database import create_db, save_city, get_popular_cities, show_user_cities
from weather import get_weather
from keyboards import get_weather_keyboard, get_history_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TGBOT_API_KEY)
dp = Dispatcher(bot)

create_db()

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    user_id = message.from_user.id
    popular_cities = get_popular_cities(user_id)

    if popular_cities:
        keyboard = get_weather_keyboard(popular_cities)
        await message.answer("Выберите город или введите новый:", reply_markup=keyboard)
    else:
        await message.answer("Введите название города для прогноза:", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text)
async def process_city(message: Message):
    city = message.text.strip()
    user_id = message.from_user.id

    weather_info = await get_weather(city)

    if "Ошибка" not in weather_info:
        save_city(user_id, city)

    await message.answer(weather_info, reply_markup=ReplyKeyboardRemove())

@dp.message_handler(commands=["history"])
async def history_command(message: Message):
    user_id = message.from_user.id
    history = show_user_cities(user_id)

    if isinstance(history, str):  # Если история пуста
        await message.answer(history)
    else:
        keyboard = get_history_keyboard(history)
        await message.answer("📜 Ваша история запросов:", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
