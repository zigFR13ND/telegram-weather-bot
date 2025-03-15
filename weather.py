import aiohttp
import logging
from config import WEATHER_API_KEY

logging.basicConfig(level=logging.INFO)

# Асинхронный запрос к OpenWeather API на текущий день
async def get_weather(city):
    """Запрашивает погоду через OpenWeather API"""
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

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


# Асинхронный запрос к OpenWeather API (5-дневный прогноз)
async def get_weather_5days(city):
    """Запрашивает погоду на 5 дней через OpenWeather API"""
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    text_weather_5days = format_weather(data)
                    return text_weather_5days
                else:
                    return "❌ Город не найден."       
    except Exception as ex:
        logging.error(f"❌ Ошибка при запросе погоды на 5 дней для {city}: {ex}")
        return "❌ Ошибка! Не удалось получить данные о погоде."
    

# Форматируем ответ API в текст для пользователя
    def format_weather(data):
        text_weather_5days = f'📍 Прогноз погоды в {data["city"]["name"]} на 5 дней:\n\n'

        days = {} # Словарь с данными прогноз погоды по дням.
        for day in data['list']:
            date = day['dt_txt'].split()[0] # Отбрасывает время, оставляем только дату 
            temp = day['main']['temp']
            if temp > 0:
                temp = f'+{temp}'
            wind = day['wind']["speed"]
            description = day["weather"][0]["description"]

            # Запоминаем только 1 прогноз в день (12:00)
            if "12:00:00" in day["dt_txt"]:
                days[date] = (temp, wind, description)

        # Формируем текст прогноза
        for date, (temp, wind, description) in days.items():
            text_weather_5days += f"📅 {date}: 🌡 {temp}°C, 💨 {wind} м/с, 🌤 {description}\n"

        return text_weather_5days
