import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# API-ключи
TGBOT_API_KEY = os.getenv("TGBOT_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not TGBOT_API_KEY or not WEATHER_API_KEY:
    raise ValueError("❌ Ошибка! Отсутствует TGBOT_API_KEY или WEATHER_API_KEY в .env")