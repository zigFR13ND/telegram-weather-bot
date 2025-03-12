import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from config import TGBOT_API_KEY
from database import create_db
from handlers import start_command, weather_command, process_city, history_command

# ✅ Включаем логирование
logging.basicConfig(level=logging.INFO)

# ✅ Создаём объект бота и диспетчера
bot = Bot(token=TGBOT_API_KEY)
dp = Dispatcher(bot)

# ✅ Создаём базу данных при запуске
create_db()

# ✅ Регистрируем обработчики
dp.register_message_handler(start_command, commands=["start"])
dp.register_message_handler(weather_command, commands=["weather"])
dp.register_message_handler(process_city, lambda message: message.text)
dp.register_message_handler(history_command, commands=["history"])

# ✅ Запускаем бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
