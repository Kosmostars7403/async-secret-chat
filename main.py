import asyncio
from datetime import datetime

import aiofiles
import configargparse


async def connect_to_chat(options):
    reader, writer = await asyncio.open_connection(
        options.host, options.port)

    while True:
        chat_message = await reader.readline()
        message_received_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        chat_message_log = f'[{message_received_time}] {chat_message.decode()}'
        print(chat_message_log)
        async with aiofiles.open(options.history, mode='a', encoding='utf-8') as file:
            await file.write(chat_message_log)


def get_application_options():
    parser = configargparse.ArgParser(default_config_files=['./config.txt'])
    parser.add('--host', help='Host for connection.')
    parser.add('--port', help='Port for connection.')
    parser.add('--history', help='Path fo history file.')

    return parser.parse_args()


if __name__ == '__main__':
    options = get_application_options()
    asyncio.run(connect_to_chat(options))