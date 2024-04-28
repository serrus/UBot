import sqlite3
import json

def json_to_db():
    print("Loading databases...")

    # Открываем файл JSON и загружаем данные
    with open('db.json', 'r') as f:
        data = json.load(f)
    print("Loaded JSON data.")

    # Создаем подключение к базе данных SQLite
    conn = sqlite3.connect('my.db')
    print("Connected to SQLite database.")

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Проходим по каждому ключу в данных JSON
    for key, values in data.items():
        # Создаем таблицу с именем ключа
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {key} (id text, value text)")
        print(f"Created table {key}.")

        # Если значения являются списком, добавляем каждое значение в таблицу
        """
        if isinstance(values, list):
            for value in values:
                cursor.execute(f"INSERT INTO {key} VALUES (?, ?)", (str(value),))
        """
        if isinstance(values, list):
            for i, value in enumerate(values):
                cursor.execute(f"INSERT INTO {key} VALUES (?, ?)", (i, str(value)))

            print(f"Inserted list values into table {key}.")

        # Если значения являются словарем, добавляем каждую пару ключ-значение в таблицу
        elif isinstance(values, dict):
            for sub_key, sub_value in values.items():
                cursor.execute(f"INSERT INTO {key} VALUES (?, ?)", (str(sub_key), str(sub_value)))
            print(f"Inserted dictionary values into table {key}.")

    # Сохраняем изменения и закрываем подключение
    conn.commit()
    conn.close()
    print("Saved changes and closed connection.")

def view_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        print(f"Table {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    json_to_db()
    view_db()
