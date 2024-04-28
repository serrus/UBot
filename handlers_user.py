# handlers_user.py
async def handle_user_commands(db_man, command, args, message):
    if command == "ad-adm":
        # Добавление администратора
        # Здесь должна быть логика добавления администратора
        if len(args) == 1:
            db_man.add_admin(args[0])
        else:
            return "Invalid arguments. Please use the format: .ad-adm <tg_id>"
        return "Admin added successfully."
    elif command == "rem-adm":
        # Удаление администратора
        # Здесь должна быть логика удаления администратора, изменение роли юзера в базе данных
        if len(args) == 1:
            # Проверяем, что пользователь с таким ID есть в базе данных
            admin = db_man.get_admin_by_id(args[0])
            if admin is None:
                return "Admin with such ID does not exist."
            
            # Изменяем роль пользователя в базе данных
            db_man.db.execute(
                "UPDATE users_auth SET role = 'user' WHERE tg_id = ?",
                (args[0],)
            )
            db_man.db.commit()
        else:
            return "Invalid arguments. Please use the format: .rem-adm <tg_id>"
        
        return "Admin removed successfully."
    elif command == "ls-adm":
        # Список администраторов
        # Здесь должна быть логика получения списка администраторов с нумерованным индексным списком, чтобы получить администратора по индексу и с ним по индексу можно было бы предпринимать дальнейшие действия: добавить администратора, удалить администратора, деактивировать администратора.
        admins = db_man.get_admins()
        if len(admins) == 0:
            return "No admins found."
        for i, admin in enumerate(admins):
            await message.reply(f"{i+1}. {admin}")
        return "List of admins."
