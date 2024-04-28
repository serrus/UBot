# handlers_forward.py
async def handle_forward_commands(db_man, command, args, message):
    if command == "ad_frw":
        # Добавление правила пересылки
        # Здесь должна быть логика добавления правила пересылки
        return "Forward rule added successfully."
    elif command == "rem-frw":
        # Удаление правила пересылки
        # Здесь должна быть логика удаления правила пересылки
        return "Forward rule removed successfully."
    elif command == "ls-frw":
        # Список правил пересылки
        # Здесь должна быть логика получения списка правил пересылки
        return "List of forward rules."
