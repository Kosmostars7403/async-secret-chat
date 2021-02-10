import asyncio
import os
import argparse

from environs import Env

from utils import setup_logger, read_message, submit_message, handle_errors, register, \
    authorize


SENDING_HOST = 'minechat.dvmn.org'
SENDING_PORT = 5050


@handle_errors
async def connect_to_chat(options):
    reader, writer = await asyncio.wait_for(connect_for_authorize(options.host, options.port), 10)

    if options.username:
        options.token = await asyncio.wait_for(register(writer, reader, logger, options.username), 10)
        reader, writer = await asyncio.wait_for(connect_for_authorize(options.host, options.port), 10)

    nickname = await authorize(writer, reader, options.token, logger)

    if not nickname:
        return

    await asyncio.wait_for(submit_message(writer, logger, options.message), 10)


@handle_errors
async def connect_for_authorize(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    server_start_message = await read_message(reader)
    logger.debug(server_start_message)

    return reader, writer


def check_token_existence():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as file:
            return file.read()
    return None


def get_application_options():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser('Minecraft chat sender.')
    parser.add_argument('message', help='Choose username for registration.')
    parser.add_argument('--host', help='Host for connection.', default=env('SENDING_HOST', SENDING_HOST))
    parser.add_argument('--port', help='Port for connection.', default=env('SENDING_PORT', SENDING_PORT))
    auth_args = parser.add_mutually_exclusive_group()
    auth_args.add_argument('--token', help='Authorization token.', default=env('TOKEN', None) or check_token_existence())
    auth_args.add_argument('--username', help='Choose username for registration.')

    return parser.parse_args()


if __name__ == '__main__':
    logger = setup_logger('sender')
    options = get_application_options()
    asyncio.run(connect_to_chat(options))
