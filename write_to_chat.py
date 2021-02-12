import asyncio
import os
import configargparse


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
    parser = configargparse.ArgParser('Minecraft chat sender.')
    parser.add('message', help='Choose username for registration.')
    parser.add('--host', help='Host for connection.', default=SENDING_HOST, env_var='SENDING_HOST')
    parser.add('--port', help='Port for connection.', default=SENDING_PORT, env_var='SENDING_PORT')
    auth_args = parser.add_mutually_exclusive_group()
    auth_args.add('--token', help='Authorization token.', default=check_token_existence(), env_var='TOKENs')
    auth_args.add('--username', help='Choose username for registration.')
    print('sdfsdf')

    return parser.parse_args()


if __name__ == '__main__':
    logger = setup_logger('sender')
    options = get_application_options()
    asyncio.run(connect_to_chat(options))
