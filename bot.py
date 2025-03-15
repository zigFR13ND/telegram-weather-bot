import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import executor
from config import TGBOT_API_KEY
from database import create_db, save_city, get_popular_cities, show_user_cities, clear_user_history
from weather import get_weather, get_weather_5days
from keyboards import get_weather_keyboard, get_history_keyboard

# Включаем логирование (чтобы видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TGBOT_API_KEY)
dp = Dispatcher(bot)

create_db()

# 🔹 /start – Приветственное сообщение
@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот для прогноза погоды. 🌤\n"
        "Напиши /weather и выбери город или введи свой.\n"
        "Можно посмотреть историю запросов: /history\n"
        "/help – Справка по командам"
    )

# 🔹 /help – Список доступных команд
@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.answer(
        "📖 Доступные команды:\n"
        "/start – Начать работу с ботом\n"
        "/weather – Узнать погоду\n"
        "/history – История запросов\n"
        "/help – Справка по командам"
        "Спасибо!"
    )

# 🔹 /weather – Запрос погоды
@dp.message_handler(commands=["weather"])
async def weather_command(message: Message):
    try:
        user_id = message.from_user.id
        popular_cities = get_popular_cities(user_id)  # Получаем ТОП-3 популярных города

        # Генерируем клавиатуру с популярными городами + кнопка "Очистить историю"
        keyboard = get_weather_keyboard(popular_cities)

        await message.answer("Введите город или выберите из популярных:", reply_markup=keyboard)
        dp.register_message_handler(get_weather_info, content_types=types.ContentType.TEXT) # Указать, как обрабатывать введенный текст пользователя после /weather
    except Exception as ex:
        logging.error(f"Ошибка в команде /weather: {ex}")
        await message.answer("Произошла ошибка! Попробуйте позже.")


# 🔹 /forecast – Запрос погоды на 5 дней
@dp.message_handler(commands=["forecast"])
async def forecast_command(message: Message):
    try:
        await message.answer("Введите город, чтобы получить прогноз на 5 дней:")
        dp.register_message_handler(get_forecast_info, content_types=types.ContentType.TEXT)
    except Exception as ex:
        logging.error(f"Ошибка в команде /forecast: {ex}")
        await message.answer("Произошла ошибка! Попробуйте позже.")
        

# 🔹 Обрабатываем ввод города (из кнопки или вручную)
async def get_weather_info(message: Message):

    try:
        city = message.text.strip()
        user_id = message.from_user.id

        # Если пользователь нажал "🗑 Очистить историю"
        if city == "🗑 Очистить историю":
            clear_user_history(user_id)
            await message.answer("✅ Ваша история запросов очищена!", reply_markup=ReplyKeyboardRemove())
            return
        
        weather_text = await get_weather(city)  # Асинхронный запрос к OpenWeather API

        if "❌" not in weather_text:  # Если город найден, сохраняем его в БД
            save_city(user_id, city)

        await message.answer(weather_text, reply_markup=ReplyKeyboardRemove())  # Отправляем ответ и убираем кнопки
        dp.unregister_message_handler(get_weather_info)  # Удаляем обработчик после ответа

    except Exception as ex:
        logging.error(f"Ошибка при запросе погоды: {ex}")
        await message.answer("Ошибка! Попробуйте позже1.")


# 🔹 Обрабатываем ввод города (из кнопки или вручную для /forecast)
async def get_forecast_info(message: Message):
    try:
        city = message.text.strip()
        user_id = message.from_user.id

        forecast_text = await get_weather_5days(city)  # Асинхронный запрос к OpenWeather API
        if "❌" not in forecast_text:
            save_city(user_id, city)

        await message.answer(forecast_text, reply_markup=ReplyKeyboardRemove())  
        dp.unregister_message_handler(get_forecast_info)  # Удаляем обработчик после ответа

    except Exception as ex:
        logging.error(f"Ошибка при запросе прогноза: {ex}")
        await message.answer("Ошибка! Попробуйте позже.")


# 🔹 /history – Показать историю городов пользователя
@dp.message_handler(commands=["history"])
async def history_command(message: Message):
    user_id = message.from_user.id
    history = show_user_cities(user_id)

    if not history:  # Если история пуста
        await message.answer("📌 У вас пока нет сохранённых городов.")
        return
    
    keyboard = get_history_keyboard(history)  # Передаём список городов, без (город, count)
    await message.answer("📜 Ваша история запросов:", reply_markup=keyboard)


# 🔹 Обрабатываем неизвестные команды
@dp.message_handler(lambda message: message.text.startswith("/"))
async def unknown_command(message: Message):
    await message.answer("❌ Неизвестная команда! Введите /help для списка доступных команд.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
