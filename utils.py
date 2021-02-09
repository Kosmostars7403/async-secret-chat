import asyncio
import json
import logging

import aiofiles
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


async def submit_message(writer, logger, message):
    logger.debug(f'Sending message: {message}')
    writer.write(message.encode(encoding='utf-8') + b'\n\n')
    await writer.drain()


async def read_message(reader):
    message = await reader.readline()
    return message.decode()


def handle_errors(async_func):
    async def wrapper(*args, **kwargs):
        try:
            result = await async_func(*args, **kwargs)
        except asyncio.TimeoutError:
            logging.error('Error with server connection!')
            raise
        return result
    return wrapper


async def register(writer, reader, logger, username):
    await submit_message(writer, logger, '')
    server_message = await read_message(reader)
    logger.debug(server_message)

    await submit_message(writer, logger, username)
    auth_response = await reader.readline()
    account_hash = json.loads(auth_response.decode())['account_hash']

    async with aiofiles.open('token.txt', mode='w', encoding='utf-8') as file:
        await file.write(account_hash)

    logger.debug(f'Your token is {account_hash}. Save it, please!')

    writer.close()
    await writer.wait_closed()

    return account_hash


async def authorize(writer, reader, token, logger):
    await asyncio.wait_for(submit_message(writer, logger, token), 10)
    auth_response = await read_message(reader)
    auth_response = json.loads(auth_response)
    if not auth_response:
        logger.error('Wrong token. Try again or register a new username.')
        return None
    logging.debug(f'Successfully authorized with nickname {auth_response["nickname"]}')
    return auth_response['nickname']