# handlers_module.py
async def handle_module_commands(db_man, command, args, message):
    if command == "ad-mod":
        # Добавление модуля
        # Здесь должна быть логика добавления модуля
        return "Module added successfully."
    elif command == "rem-mod":
        # Удаление модуля
        # Здесь должна быть логика удаления модуля
        return "Module removed successfully."
    elif command == "ls-mod":
        # Список модулей
        # Здесь должна быть логика получения списка модулей
        return "List of modules."
