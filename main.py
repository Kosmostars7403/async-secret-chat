import asyncio
from datetime import datetime

import aiofiles


async def connect_to_chat(message):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        chat_message = await reader.readline()
        message_received_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        chat_message_log = f'[{message_received_time}] {chat_message.decode()}'
        print(chat_message_log)
        async with aiofiles.open('chat_log.txt', mode='a', encoding='utf-8') as file:
            await file.write(chat_message_log)


if __name__ == '__main__':
    asyncio.run(connect_to_chat('Hello World!'))