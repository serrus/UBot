# handlers_city.py
async def handle_city_commands(db_man, command, args, message):
    if command == "ad-cty":
        # Добавление города
        # Здесь должна быть логика добавления города
        return "City added successfully."
    elif command == "rem-cty":
        # Удаление города
        # Здесь должна быть логика удаления города
        return "City removed successfully."
    elif command == "ls-cty":
        # Список городов
        # Здесь должна быть логика получения списка городов
        return "List of cities."
