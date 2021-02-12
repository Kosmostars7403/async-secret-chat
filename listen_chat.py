import asyncio
from datetime import datetime
import configargparse

import aiofiles

from chat_tools import read_message, connect_to_chat
from utils import setup_logger


LISTENING_HOST = 'minechat.dvmn.org'
LISTENING_PORT = 5000
CHAT_LOG_PATH = 'chat_log.txt'


async def main(options):
    async with connect_to_chat(options.host, options.port, logger) as (reader, writer):
        while True:
            chat_message = await asyncio.wait_for(read_message(reader), 10)
            message_received_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            chat_message = f'[{message_received_time}] {chat_message}'
            print(chat_message)
            async with aiofiles.open(options.history, mode='a', encoding='utf-8') as file:
                await file.write(chat_message)


def get_application_options():
    parser = configargparse.ArgParser('Minecraft chat listener.')

    parser.add('--host', help='Host for connection.', default=LISTENING_HOST, env_var='LISTENING_HOST')
    parser.add('--port', help='Port for connection.', default=LISTENING_PORT, env_var='LISTENING_PORT')
    parser.add('--history', help='Path for history file.', default=CHAT_LOG_PATH, env_var='CHAT_LOG_PATH')

    return parser.parse_args()


if __name__ == '__main__':
    logger = setup_logger('listener')
    options = get_application_options()
    asyncio.run(main(options))