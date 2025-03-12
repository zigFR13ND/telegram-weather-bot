import logging
from aiogram import types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import save_city, get_popular_cities, show_user_cities
from weather import get_weather

### ✅ **Команда /start**
async def start_command(message: Message):
    await message.answer("Привет! Я бот для прогноза погоды. Напиши /weather, чтобы узнать погоду.")

### ✅ **Команда /weather (предлагаем популярные города)**
async def weather_command(message: Message):
    user_id = message.from_user.id
    popular_cities = get_popular_cities(user_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if popular_cities:
        for city in popular_cities:
            keyboard.add(KeyboardButton(city))  # ✅ Добавляем кнопки с городами
        keyboard.add(KeyboardButton("🌍 Ввести другой город"))
        await message.answer("Выберите город или введите новый:", reply_markup=keyboard)
    else:
        await message.answer("Введите название города для прогноза:", reply_markup=ReplyKeyboardRemove())

### ✅ **Обрабатываем ввод города (асинхронный запрос погоды)**
async def process_city(message: Message):
    city = message.text.strip()
    user_id = message.from_user.id

    weather_info = await get_weather(city)  # ✅ Асинхронный вызов

    if "Ошибка" not in weather_info:
        save_city(user_id, city)  # ✅ Сохраняем город в базу

    await message.answer(weather_info, reply_markup=ReplyKeyboardRemove())

### ✅ **Команда /history (отображаем историю)**
async def history_command(message: Message):
    user_id = message.from_user.id
    history = show_user_cities(user_id)

    await message.answer(history)
