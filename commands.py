# commands.py
import database
from permissions import PermissionManager  # Импортируем класс PermissionManager
from handlers_user import handle_user_commands
from handlers_group import handle_group_commands
from handlers_city import handle_city_commands
from handlers_id import handle_id_commands
from handlers_trigger import handle_trigger_commands
from handlers_forward import handle_forward_commands
from handlers_module import handle_module_commands
from regex import role_id_from_string
import shlex  # добавляем этот импорт в начало файла
import re



async def handle_command(command, args, message):
    db = database.get_db()
    #db_man = database.PermissionManager(database.get_db())
    #db_man = PermissionManager(database.get_db())  # Создаем экземпляр PermissionManager с базой данных
    db_man = permission_manager

    # заменяем запятые на пробелы и разбиваем строку на команду и аргументы
    command_and_args = shlex.split(input_string.replace(',', ' '))
    command = command_and_args[0]
    args = command_and_args[1:]


    #if command == "start":
    #    return "Bot started!"
    if command == "start":
        user_id = message.from_user.id
        if db_man.check_user_registration(user_id):
            if db_man.check_user_active(user_id):
                # Пользователь уже зарегистрирован и активен
                return "Welcome back! You are already registered and active."
            else:
                # Пользователь уже зарегистрирован, но неактивен
                return "You are registered but not active. Please contact an admin."

        # Предложить пользователю включить уведомления
        keyboard = [["Yes", "No"]]
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        return f"Hello! Would you like to receive notifications? Please choose Yes or No.", reply_markup

        # Добавление пользователя
    elif command == "ad-usr":
        if len(args) >= 3:
            tg_id = args[0]
            name = args[1]
            city = args[2]
            location = None
            trigger_words = []
            role_id = 5  # по умолчанию роль - 'user'
            # обработка необязательных аргументов
            for arg in args[3:]:
                #if arg.startswith('/'):  # это роль
                if re.match(r'^/\w+$', arg):  # это роль
                    role_id = role_id_from_string(arg[1:])  # получить id роли из строки
                elif location is None:  # это местоположение
                    location = arg
                else:  # это ключевое слово
                    trigger_words.append(arg)
            # добавление пользователя
            database.add_user(tg_id, name, city, location, trigger_words, notification_enabled=False, active=True, role_id=role_id)
            return f"User {name} from {city} added successfully."
        else:
            return "Invalid arguments. Please use the format:\n.ad-usr [tg_id] [name] [city] [/role] [location] [trigger_word_1] [trigger_word_2] ..."

    elif command == "help":
        # Формирование списка команд с их описаниями
        commands_list = db['COMMANDS']  # Замените на актуальный путь к командам в вашей БД
        help_message = "**Список доступных команд:**\n"
        for cmd, desc in commands_list.items():
            # Экранируем специальные символы в cmd и desc, если они там есть
            safe_cmd = cmd.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
            safe_desc = desc.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
            help_message += f"• `.{cmd}` - {desc}\n"
        return help_message

    elif command == "cst":
        print("Режим копирования из БД:", database.get_copy_mode())
        mode = database.toggle_copy_mode(True)
        print("cst mode:", mode)
        print("Режим копирования после переключения:", database.get_copy_mode())
        response = "Copy mode is now enabled." if mode else "Failed to enable copy mode."
        print(f"Response for command {command}: {response}")  # Вывод ответа
        return mode
    
    elif command == "csp":
        print("Режим копирования из БД:", database.get_copy_mode())
        mode = database.toggle_copy_mode(False)
        print("csp mode:", mode)
        print("Режим копирования после переключения:", database.get_copy_mode())
        #response = "Copy mode is now disabled." if not mode else "Failed to disable copy mode."
        response = "Copy mode is now disabled." if mode == False else "Failed to disable copy mode."
        print(f"Response for command {command}: {response}")  # Вывод ответа
        #return response
        return mode
    elif command == "cs":
        mode = database.get_copy_mode()
        print("cs mode:", mode)
        response = "Copy mode is currently enabled." if mode else "Copy mode is currently disabled."
        print(f"Response for command {command}: {response}")  # Вывод ответа
        return response
    elif command == "ad-adm":
        # Обработка команды ad-adm
        response = db_man.admin_duties(message.from_user.id, "add", {"USER_GROUPS": {"admin": [args[0]]}})
        return response
    elif command == "rem-adm":
        # Обработка команды rem-adm
        response = db_man.admin_duties(message.from_user.id, "remove", {"USER_GROUPS": {"admin": [args[0]]}})
        return response
    elif command == "ad-grp":
        # Обработка команды ad-grp
        new_group = {"name": args[0], "description": args[1], "forwarding_rules": {}, "members": []}
        response = db_man.admin_duties(message.from_user.id, "add", {"GROUPS": [new_group]})
        return response
    elif command == "rem-grp":
        # Обработка команды rem-grp
        response = db_man.admin_duties(message.from_user.id, "remove", {"GROUPS": [{"name": args[0]}]})
        return response
    elif command == "ls-grp":
        # Обработка команды ls-grp
        groups = db_man.get_groups()
        response = "List of groups:\n"
        for group in groups:
            response += f"- {group['name']}: {group['description']}\n"
        return response

    # Добавьте здесь обработку других команд


    # Добавьте здесь обработку других команд
    else:
        return "Unknown command!"

    """
    elif command == "cst":
        mode = database.toggle_copy_mode(True)
        return "Copy mode is now enabled." if mode else "Failed to enable copy mode."
    elif command == "csp":
        mode = database.toggle_copy_mode(False)
        return "Copy mode is now disabled." if not mode else "Failed to disable copy mode."
    elif command == "cs":
        mode = database.get_copy_mode()
        return "Copy mode is currently enabled." if mode else "Copy mode is currently disabled."
    """