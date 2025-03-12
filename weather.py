import aiohttp
import logging
from config import WEATHER_API_KEY

async def get_weather(city):
    """Запрашивает погоду через OpenWeather API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["main"]["temp"]
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
        logging.error(f"Ошибка запроса к OpenWeather: {e}")
        return "❌ Ошибка! Не удалось получить данные о погоде."
