import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import executor
from config import TGBOT_API_KEY
from database import create_db, save_city, get_popular_cities, show_user_cities, clear_user_history
from weather import get_weather
from keyboards import get_weather_keyboard, get_history_keyboard

# ✅ Включаем логирование (чтобы видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

# ✅ Создаём бота и диспетчер
bot = Bot(token=TGBOT_API_KEY)
dp = Dispatcher(bot)

create_db()

# 🔹 /start – Приветственное сообщение
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот для прогноза погоды. 🌤\n"
        "Напиши /weather и выбери город или введи свой.\n"
        "Можно посмотреть историю запросов: /history"
    )

# 🔹 /weather – Запрос погоды
@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    user_id = message.from_user.id
    popular_cities = get_popular_cities(user_id)  # 📌 Получаем ТОП-3 популярных города

    # ✅ Генерируем клавиатуру с популярными городами + кнопка "Очистить историю"
    keyboard = get_weather_keyboard(popular_cities)

    await message.answer("Введите город или выберите из популярных:", reply_markup=keyboard)

# 🔹 Обрабатываем ввод города (из кнопки или вручную)
@dp.message_handler()
async def get_weather_info(message: Message):
    city = message.text.strip()
    user_id = message.from_user.id

    # ✅ Если пользователь нажал "🗑 Очистить историю"
    if city == "🗑 Очистить историю":
        clear_user_history(user_id)
        await message.answer("✅ Ваша история запросов очищена!", reply_markup=ReplyKeyboardRemove())
        return

    try:
        weather_text = await get_weather(city)  # ⚡ Асинхронный запрос к OpenWeather API

        if "❌" not in weather_text:  # ✅ Если город найден, сохраняем его в БД
            save_city(user_id, city)
    except Exception as e:
        weather_text = f"❌ Ошибка при запросе погоды: {e}"

    await message.answer(weather_text, reply_markup=ReplyKeyboardRemove())  # ✅ Отправляем ответ и убираем кнопки

# 🔹 /history – Показать историю городов пользователя
@dp.message_handler(commands=["history"])
async def history_command(message: Message):
    user_id = message.from_user.id
    history = show_user_cities(user_id)

    # ✅ Генерируем кнопки с историей + "Очистить историю"
    keyboard = get_history_keyboard(history)

    await message.answer(history, reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
