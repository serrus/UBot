# copy_message.py
from database import get_db, get_copy_mode
from pyrogram import Client, filters
import logging

#async def forward_message(client: Client, message):
async def forward_message(client, message):
    DB = get_db()  # Получаем текущее состояние базы данных
    copy_mode = get_copy_mode()  # Получаем текущее состояние режима копирования
    print(f"copy_mode: {copy_mode}")
    if copy_mode and message.chat.id not in DB['FORWARD_GROUPS']['group_ignore']:
        print(f"Копирую сообщение из {message.chat.id} в {DB['FORWARD_GROUPS']['group_all']}")
        try:
            # Проверка на наличие id
            if hasattr(message, 'id'):
                print(f"Копирую сообщение с id : {message.id}")
                # Проверка, что исходный чат не является группой, в которую пересылаются все сообщения
                if message.chat.id != DB['FORWARD_GROUPS']['group_all']:
                    # Сбор информации о сообщении
                    info = f"**Информация о сообщении:**\n"
                    info += f"Откуда: `{message.chat.id}`\n"
                    # chat_title = chat_info.title if chat_info.title else "Название группы неизвестно"
                    chat_info = await client.get_chat(message.chat.id)  # Получаем информацию о чате
                    chat_title = chat_info.title if chat_info.title else "Название группы неизвестно"
                    info += f"Название чата: `{chat_title}`\n"
                    info += f"ID сообщения: `{message.id}`\n"
                    # Получение информации о пользователе
                    if message.from_user:
                        info += f"ID пользователя: `{message.from_user.id}`\n"
                        info += f"Имя пользователя: `{message.from_user.first_name}`"
                        if message.from_user.last_name:
                            info += f" {message.from_user.last_name}\n"
                        else:
                            info += "\n"
                        if message.from_user.username:
                            info += f"Имя пользователя: `{message.from_user.username}`\n"
                    # Создание ссылки на сообщение в группе
                    message_link = message.link
                    print(f"message_link: {message_link}")
                    text = message.text or ""
                    print(f"text: {text}")
                    # Экранируем специальные символы Markdown в тексте сообщения
                    escaped_text = text.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
                    # Отправляем сообщение в группу group_all
                    await client.send_message(
                        chat_id=DB['FORWARD_GROUPS']['group_all'],
                        text=f"{info}\n\n`{escaped_text}`\n\nСсылка на оригинальное сообщение\n{message_link}"
                    )
                    print(f" type(DB['FORWARD_GROUPS']['group_all']): {type(DB['FORWARD_GROUPS']['group_all'])}")
                    #chat_id = int(DB['FORWARD_GROUPS']['group_all'])
                    #print(f"chat_id: {chat_id}")
                    logging.info(f"Chat ID: {DB['FORWARD_GROUPS']['group_all']}")
                    #await client.send_message(chat_id=DB['FORWARD_GROUPS']['group_all'], text=f"{info}\n\n`{text}`\n\nСсылка на оригинальное сообщение {message_link}", parse_mode=None)

                    print(f"Сообщение из {message.chat.id} успешно скопировано в {DB['FORWARD_GROUPS']['group_all']}")
                else:
                    print(f"Сообщение из {message.chat.id} не копируется, так как это тот же чат")
            else:
                print(f"Сообщение из {message.chat.id} не может быть скопировано, так как оно не содержит id")
        except Exception as e:
            # Вывод информации об ошибке при копировании сообщения
            print(f"Ошибка при копировании сообщения из {message.chat.id} в {DB['FORWARD_GROUPS']['group_all']}: {e}")
