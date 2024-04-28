# database.py
import json

db_file = 'db.json'
db_data = {}

def load_db():
    global db_data
    try:
        with open(db_file, 'r', encoding='utf-8') as f:  # Указываем кодировку UTF-8 здесь
            db_data = json.load(f)
    except FileNotFoundError:
        print(f"Файл {db_file} не найден.")
        db_data = {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании файла {db_file}: {e}")
        db_data = {}

def save_db():
    try:
        with open(db_file, 'w', encoding='utf-8') as f:  # Указываем кодировку UTF-8 здесь
            json.dump(db_data, f, ensure_ascii=False, indent=4)  # ensure_ascii=False позволяет сохранять не ASCII символы в их истинном виде
    except Exception as e:
        print(f"Ошибка при сохранении файла {db_file}: {e}")

def toggle_copy_mode1(mode):
    db_data['FORWARD_GROUPS']['fwAll_enabled'] = mode
    #print(f"Saving database to file: {db_file}")
    #print(f"Database contents: {db_data}")
    save_db()  # Сохраняем обновленное состояние в файл
    return "Copy mode is on" if mode else "Copy mode is off"


def toggle_copy_mode(mode):
    #current_mode = db_data['FORWARD_GROUPS']['fwAll_enabled']
    current_mode = db_data['GLOBAL_SETTINGS']['forwarding_rules']['fwAll_enabled']

    print("000 Copy mode from DB:", current_mode)
    print("111 Copy mode from DB:", mode)
    if current_mode == mode:  # Если требуемое состояние уже установлено, выходим из функции без записи в БД
        print("222-1 current_mode == mode:", current_mode == mode)
        return f"Copy mode is already {'on' if mode else 'off'}"

    print("333 current_mode != mode:", current_mode != mode)
    print("444 mode:", mode)
    print("555 current_mode:", current_mode)

    # Обновляем состояние в БД
    #db_data['FORWARD_GROUPS']['fwAll_enabled'] = mode
    db_data['GLOBAL_SETTINGS']['forwarding_rules']['fwAll_enabled'] = mode


    # Сохраняем обновленное состояние в БД
    save_db()

    return f"Copy mode is now {'on' if mode else 'off'}"

    #return "Copy mode is now enabled." if mode else "Copy mode is now disabled."



def get_copy_mode():
    #return db_data['FORWARD_GROUPS']['fwAll_enabled']
    #mode = db_data['FORWARD_GROUPS']['fwAll_enabled']
    #mode = db_data['GLOBAL_SETTINGS']['forwarding_rules']['fwAll_enabled']
    #return db_data['GLOBAL_SETTINGS']['forwarding_rules']['fwAll_enabled']
    mode = db_data['GLOBAL_SETTINGS']['forwarding_rules']['fwAll_enabled']
    print("123 Copy mode from DB:", mode)
    return mode


# функции для управления пользователями и их активностью
#def add_user(user_id, name, city):
def permission_manager.add_user(tg_id, name, city, location, trigger_words, notification_enabled=False, active=True):
    user_id = str(user_id)
    db_data.setdefault('users', {})[user_id] = {
        "name": name,
        "city": city,
        "active": True,
        "registered": False
    }
    save_db()

def set_user_active(user_id, active):
    user_id = str(user_id)
    if user_id in db_data.get('users', {}):
        db_data['users'][user_id]['active'] = active
        save_db()

def register_user(user_id):
    user_id = str(user_id)
    if user_id in db_data.get('users', {}):
        db_data['users'][user_id]['registered'] = True
        save_db()

def check_user_registration(user_id):
    user_id = str(user_id)
    return db_data.get('users', {}).get(user_id, {}).get('registered', False)

def get_user_data(user_id):
    user_id = str(user_id)
    return db_data.get('users', {}).get(user_id, {})

# Records the activity of a user in a log file.
def record_user_activity(user_id, data_changed):
    user_id = str(user_id)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"uid/{user_id}", 'a', encoding='utf-8') as user_file:  # Указываем кодировку UTF-8 здесь
        user_file.write(f"{timestamp}: {data_changed}\n")



def get_db():
    return db_data

def update_db(key, value):
    db_data[key] = value


