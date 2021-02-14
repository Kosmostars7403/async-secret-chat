import asyncio
import logging

import configargparse

from auth_tools import authorize, register, check_token_existence
from chat_tools import connect_to_chat, submit_message

SENDING_HOST = 'minechat.dvmn.org'
SENDING_PORT = 5050

logger = logging.getLogger('sender')


async def main(options):
    logger.debug(f'Started sending message to chat on {options.host}:{options.port}')
    if options.username:
        async with connect_to_chat(options.host, options.port) as (reader, writer):
            options.minechat_token = await register(writer, reader, options.username)
    if options.minechat_token:
        async with connect_to_chat(options.host, options.port) as (reader, writer):
            nickname = await authorize(writer, reader, options.minechat_token)
            if not nickname:
                return
            await submit_message(writer, options.message)


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
    logging.basicConfig(level=logging.DEBUG)
    options = get_application_options()
    asyncio.run(main(options))
