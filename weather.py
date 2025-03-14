import aiohttp
import logging
from config import WEATHER_API_KEY

logging.basicConfig(level=logging.INFO)

# Асинхронный запрос к OpenWeather API
async def get_weather(city):
    """Запрашивает погоду через OpenWeather API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
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

    except Exception as ex:
        logging.error(f"❌ Ошибка при запросе погоды для {city}: {ex}")
        return "❌ Ошибка! Не удалось получить данные о погоде."

