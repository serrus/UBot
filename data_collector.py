    # data_collector.py
async def collect_data(client, message):
    data_id, *data = message.text.split('\n', 1)
    existing_message = await search_message_by_id(data_id, TARGET_GROUP_ID, client)
    if existing_message:
        # Проверяем и обновляем данные, если нужно
        updated_message = update_data(existing_message, data)
        await client.edit_message_text(TARGET_GROUP_ID, existing_message.message_id, updated_message)
    else:
        # Создаем новое сообщение с данными
        await client.send_message(TARGET_GROUP_ID, message.text)

async def search_message_by_id(data_id, group_id, client):
    async for message in client.iter_history(group_id):
        if message.text and message.text.startswith(data_id):
            return message
    return None

def update_data(existing_message, new_data):
    # Добавляем новые данные к существующему сообщению
    updated_message_text = existing_message.text + "\n" + new_data
    return updated_message_text


    # Возможно, другие вспомогательные функции
async def print_user_info(client, user_id):
    user_info = await client.get_users(user_id)
    print("\nИнформация о пользователе:\n")
    for attribute in dir(user_info):
        value = getattr(user_info, attribute)
        print(f"{attribute}: {value}")

async def print_chat_info(client, chat_id):
    chat_info = await client.get_chat(chat_id)
    print("\nИнформация о чате:\n")
    for attribute in dir(chat_info):
        value = getattr(chat_info, attribute)
        print(f"{attribute}: {value}")
