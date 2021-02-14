import asyncio

import configargparse

from auth_tools import authorize, register
from chat_tools import connect_to_chat, submit_message
from utils import setup_logger, check_token_existence

SENDING_HOST = 'minechat.dvmn.org'
SENDING_PORT = 5050


async def main(options):
    if options.username:
        async with connect_to_chat(options.host, options.port, logger) as (reader, writer):
            options.token = await register(writer, reader, logger, options.username)
    if options.token:
        async with connect_to_chat(options.host, options.port, logger) as (reader, writer):
            nickname = await authorize(writer, reader, options.token, logger)
            if not nickname:
                return
            await submit_message(writer, logger, options.message)


def get_application_options():
    parser = configargparse.ArgParser('Minecraft chat sender.')

    parser.add('message', help='Choose username for registration.')
    parser.add('--host', help='Host for connection.', default=SENDING_HOST, env_var='SENDING_HOST')
    parser.add('--port', help='Port for connection.', default=SENDING_PORT, env_var='SENDING_PORT')
    auth_args = parser.add_mutually_exclusive_group()
    auth_args.add('--minechat_token', help='Authorization token.', default=check_token_existence(), env_var='MINECHAT_TOKEN')
    auth_args.add('--username', help='Choose username for registration.')

    return parser.parse_args()


if __name__ == '__main__':
    logger = setup_logger('sender')
    options = get_application_options()
    asyncio.run(main(options))
