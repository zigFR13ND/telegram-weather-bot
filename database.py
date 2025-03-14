import sqlite3
import logging

# Функция для создания базы данных (если её нет)
def create_db():
    try:
        conn = sqlite3.connect("weather_bot.db")  # Подключаемся к файлу базы данных
        cursor = conn.cursor()  # Создаём "курсор" (он выполняет SQL-запросы)
        
        # Создаём таблицу, если её нет
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                user_id INTEGER,  -- ID пользователя в Телеграме
                city TEXT,        -- Город, который он вводил
                count INTEGER DEFAULT 1,  -- Сколько раз он вводил этот город
                PRIMARY KEY (user_id, city)  -- Уникальный ключ: ID пользователя + город
            )
        """)
        
        conn.commit()  # Сохраняем изменения
        conn.close()   # Закрываем соединение
    except Exception as ex:
        logging.error(f'Ошибка при создании базы: {ex}')


# Функция для сохранения города
def save_city(user_id, city):
    try:
        conn = sqlite3.connect("weather_bot.db")  # Подключаемся к базе
        cursor = conn.cursor()  # Создаём "курсор" для SQL-запросов

        # Проверяем, вводил ли пользователь этот город раньше
        cursor.execute("SELECT count FROM cities WHERE user_id = ? AND city = ?", (user_id, city))
        row = cursor.fetchone()  # Получаем результат

        if row:
            # Если город уже вводился, увеличиваем счётчик
            cursor.execute("UPDATE cities SET count = count + 1 WHERE user_id = ? AND city = ?", (user_id, city))
        else:
            # ➕ Если новый город – добавляем его в базу
            cursor.execute("INSERT INTO cities (user_id, city) VALUES (?, ?)", (user_id, city))

        conn.commit()  # Сохраняем изменения
        conn.close()   # Закрываем соединение
    except Exception as ex:
        logging.error(f'Ошибка при сохранении города {city}: {ex}')        


# Функция для получения популярных городов (топ-3)
def get_popular_cities(user_id):
    try:
        conn = sqlite3.connect("weather_bot.db")
        cursor = conn.cursor()

        # Берём ТОП-3 самых популярных города для пользователя
        cursor.execute("SELECT city FROM cities WHERE user_id = ? ORDER BY count DESC LIMIT 3", (user_id,))
        cities = [row[0] for row in cursor.fetchall()]  # 📌 Преобразуем результат в список

        conn.close()
        return cities  # Вернёт список городов (например, ["Москва", "Казань", "Питер"])
    except Exception as ex:
        logging.error(f'Ошибка при получении популярных городов пользователя: {ex}')           

# ✅ Функция для получения всех городов пользователя
def show_user_cities(user_id):
    try:
        conn = sqlite3.connect("weather_bot.db")
        cursor = conn.cursor()

        cursor.execute("SELECT city FROM cities WHERE user_id = ? ORDER BY count DESC", (user_id,))
        rows = cursor.fetchall()  # Получаем все записи

        conn.close()  # Закрываем соединение

        if not rows:
            return []  # Возвращаем ПУСТОЙ список вместо строки!
        
        result = "📌 Ваши города:\n"

        return [row[0] for row in rows]  # список городов!
    except Exception as ex:
        logging.error(f'Ошибка при получении всех городов: {ex}')
        return "❌ Ошибка базы данных!"

def clear_user_history(user_id):
    """Очищает всю историю пользователя"""
    conn = sqlite3.connect("weather_bot.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cities WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()