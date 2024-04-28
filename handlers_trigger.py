# handlers_trigger.py
async def handle_trigger_commands(db_man, command, args, message):
    if command == "ad-trg":
        # Добавление триггера
        # Здесь должна быть логика добавления триггера
        return "Trigger added successfully."
    elif command == "rem-trg":
        # Удаление триггера
        # Здесь должна быть логика удаления триггера
        return "Trigger removed successfully."
    elif command == "ls-trg":
        # Список триггеров
        # Здесь должна быть логика получения списка триггеров
        return "List of triggers."
