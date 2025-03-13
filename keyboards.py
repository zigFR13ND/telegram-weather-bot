from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_weather_keyboard(popular_cities):
    """Создаёт клавиатуру с популярными городами"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in popular_cities:
        keyboard.add(KeyboardButton(city))
    keyboard.add(KeyboardButton("🌍 Ввести другой город"))
    return keyboard

def get_history_keyboard(history):
    """Создаёт клавиатуру с историей запросов"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for city in history:
        keyboard.add(KeyboardButton(city))
    keyboard.add(KeyboardButton("❌ Очистить историю"))
    return keyboard
