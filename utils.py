import asyncio
import logging
from datetime import datetime

import configargparse


def setup_logger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    return logger


def get_application_options():
    parser = configargparse.ArgParser(default_config_files=['./config.txt'])
    parser.add('--host', help='Host for connection.')
    parser.add('--port', help='Port for connection.')
    parser.add('--history', help='Path for history file.')

    return parser.parse_args()


async def send_message(writer, logger, message):
    logger.debug(f'Sending message: {message}')
    writer.write(message.encode(encoding='utf-8') + b'\n\n')
    await writer.drain()


async def read_message(reader, logger):
    message_received_time = datetime.now().strftime('%d.%m.%y %H:%M:%S')
    message = await reader.readline()
    message = f'[{message_received_time}] {message.decode()}'
    logger.debug(message)
    return message


def handle_errors(async_func):
    async def wrapper(*args, **kwargs):
        try:
            result = await async_func(*args, **kwargs)
        except asyncio.TimeoutError:
            logging.error('Error with server connection!')
            raise
        return result
    return wrapper


