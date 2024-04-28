# handlers_id.py
async def handle_id_commands(db_man, command, args, message):
    if command == "ad-id":
        # Добавление ID
        # Здесь должна быть логика добавления ID
        return "ID added successfully."
    elif command == "rem-id":
        # Удаление ID
        # Здесь должна быть логика удаления ID
        return "ID removed successfully."
    elif command == "ls-id":
        # Список ID
        # Здесь должна быть логика получения списка ID
        return "List of IDs."
