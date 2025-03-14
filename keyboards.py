from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ✅ Генерируем клавиатуру с популярными городами
def get_weather_keyboard(cities):
    """Создаёт клавиатуру с популярными городами"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for city in cities:
        keyboard.add(KeyboardButton(city)) # 📌 Добавляем кнопки с городами

    keyboard.add(KeyboardButton("🗑 Очистить историю")) # 📌 Кнопка для очистки истории
    return keyboard

# ✅ Генерируем клавиатуру для истории запросов
def get_history_keyboard(history):
    """Создаёт клавиатуру с историей запросов"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for city in history:
        keyboard.add(KeyboardButton(city))  # ✅ Теперь кнопки создаются корректно!

    keyboard.add(KeyboardButton("🗑 Очистить историю"))
    return keyboard
