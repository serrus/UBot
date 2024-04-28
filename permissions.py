# permissions.py
class PermissionManager:
    def __init__(self, db):
        self.db = db


    # Проверка роли пользователя
    def check_user_role(self, user_id):
        user_info = self.db["USERS"].get(str(user_id), {})
        user_role_id = user_info.get("role_id", 5)  # По умолчанию присваиваем роль "user"
        user_role = self.db["USER_GROUPS"].get(str(user_role_id), {}).get("name", "user")
        return user_role

    # Изменение данных пользователя
    def modify_user_data(self, user_id, new_data):
        role = self.check_user_role(user_id)
        if role in ["admin", "owner"]:
            user_data = self.db["USERS"].get(str(user_id))
            if user_data:
                user_data.update(new_data)
                save_db()  # Сохраняем изменения в базу данных
                return "User data updated"
            else:
                return "User not found"
        else:
            return "Permission error: User can only modify own data"

    # Изменение данных группы
    def modify_group_data(self, user_id, group_index, new_data):
        role = self.check_user_role(user_id)
        if role == "manager":
            group_data = self.db["GROUPS_DICTIONARY"].get(group_index)
            if group_data:
                group_data.update(new_data)
                save_db()  # Сохраняем изменения в базу данных
                return "Group data updated"
            else:
                return "Group not found"
        else:
            return "Permission error: Only managers can modify group data"

    # Обязанности администратора
    def admin_duties(self, user_id, command, new_data):
        role = self.check_user_role(user_id)
        if role == "admin":
            if command == "add":
                self.db["GROUPS_DICTIONARY"].update(new_data)
                save_db()  # Сохраняем изменения в базу данных
            elif command == "remove":
                for key in new_data.keys():
                    if key in self.db["GROUPS_DICTIONARY"]:
                        del self.db["GROUPS_DICTIONARY"][key]
                save_db()  # Сохраняем изменения в базу данных
            return "Database updated"
        else:
            return "Permission error: Only admins can update the database"

    # Обязанности владельца
    def owner_duties(self, user_id, command, target_user_id):
        role = self.check_user_role(user_id)
        if role == "owner":
            if command == "add":
                self.db["USERS"][str(target_user_id)]["role_id"] = 2  # Присваиваем роль админа
            elif command == "remove":
                self.db["USERS"][str(target_user_id)]["role_id"] = 5  # Присваиваем роль пользователя
            save_db()  # Сохраняем изменения в базу данных
            return "User role updated"
        else:
            return "Permission error: Only owners can update user roles"

    
    #def add_user(self, tg_id, role_id=5):
        self.db.setdefault('users', {})[str(tg_id)] = {"role_id": role_id}
    
    def add_user(self, tg_id, role_id=5):
        print(f"Adding user with tg_id={tg_id} and role_id={role_id}")
        self.db.setdefault('users', {})[str(tg_id)] = {"role_id": role_id}
        print(f"Current state of the database: {self.db}")
