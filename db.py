import sqlite3

# Создание и подключение к базе данных
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()

# Создание таблицы для тем
cursor.execute('''
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

# Создание таблицы для задач с новыми полями
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    topic_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'невыполнена',
    FOREIGN KEY (topic_id) REFERENCES topics (id)
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
