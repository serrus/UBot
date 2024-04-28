# main.py
from pyrogram import Client, filters
import os
import logging
import database
import commands
from dotenv import load_dotenv
from copy_message import forward_message
from data_collector import collect_data
from data_collector import print_user_info, print_chat_info
from permissions import PermissionManager

permission_manager = PermissionManager()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

database.load_db()  # Загрузка БД при запуске

# Загружаем данные из базы данных
db = database.get_db()
# вывести в лог считанную db
#print (f"БД db.json : {db}")

# Получаем список администраторов на основании их role_id
admins = [user["tg_id"] for user in db["USERS"].values() if user["role_id"] == 2]

# Получаем необходимые значения из базы данных
# SOURCE_GROUP_ID = db['FORWARD_GROUPS']['source_group_ids']
SOURCE_GROUP_ID = db['GLOBAL_SETTINGS']['forwarding_rules']['source_group_indices']
#TARGET_GROUP_ID = db['FORWARD_GROUPS']['target_group_id']
TARGET_GROUP_ID = db['GLOBAL_SETTINGS']['forwarding_rules']['target_group_id']


bot = Client("user_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

#@bot.on_message(filters.command(list(database.get_db()['COMMANDS'].keys()), prefixes=".") & filters.user(database.get_db()['ADMINS']))
# Обработчик получаемых команд
@bot.on_message(filters.command(list(database.get_db()['COMMANDS'].keys()), prefixes=".") & filters.user(admins))
async def command_listener(client, message):
    command = message.command[0]
    print(f"Received command: {command}")  # Вывод полученной команды
    args = message.command[1:]
    # В вашем обработчике команд
    response = await commands.handle_command(command, args, message)
    print(f"Response command: {response}")  # Вывод ответа
    #await message.reply_text(response)
    try:
        await message.reply_text(response)
    except Exception as e:
        print(f"Failed to send message: {e}")  # Вывод ошибки, если она возникает



# Здесь можно добавить другие обработчики сообщений...

# В main.py, после объявления command_listener или в любом другом месте до bot.run()
# Обработчик для пересылки всех входящих сообщений юзер-бота:
@bot.on_message(filters.private | filters.group & ~filters.me)
async def message_listener(client, message):
    await forward_message(client, message)


# Обработчик для пересылки сообщений по триггерным словам и ID:
@bot.on_message(filters.chat(SOURCE_GROUP_ID))
async def trigger_word_listener(client, message):
    triggers = database.get_db()['TRIGGERS']
    if any(trigger in message.text for trigger in triggers['words']) and (message.from_user.id in triggers['user_ids'] if message.from_user else False):
        await message.forward(TARGET_GROUP_ID)


# Обработчик для сбора данных в группу по ID:
@bot.on_message(filters.chat(TARGET_GROUP_ID))
async def data_collector_listener(client, message):
    await collect_data(client, message, TARGET_GROUP_ID)


# Предположим, что message - это ваш объект Message
# Выводим информацию о том, что message содержит
#@bot.on_message(group=-1) # - работает
#@bot.on_message() # - не работает
async def handle_message(client, message):
    print("Атрибуты и их значения для объекта Message:")
    for attribute in dir(message):
        value = getattr(message, attribute)
        print(f"{attribute}: {value}")
    #return False


#@bot.on_message(group=-1)
async def handle_message(client, message):
    await print_user_info(client, message.from_user.id)
    await print_chat_info(client, message.chat.id)


# вывести сообщение в консоль
print("Starting bot...")
bot.run()