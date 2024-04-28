# handlers_group.py
async def handle_group_commands(db_man, command, args, message):
    if command == "ad-grp":
        # Добавление группы
        # Здесь должна быть логика добавления группы
        return "Group added successfully."
    elif command == "rem-grp":
        # Удаление группы
        # Здесь должна быть логика удаления группы
        return "Group removed successfully."
    elif command == "ls-grp":
        # Список групп
        # Здесь должна быть логика получения списка групп
        return "List of groups."
