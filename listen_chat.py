import asyncio

import aiofiles

from utils import setup_logger, get_application_options, read_message, handle_errors


@handle_errors
async def connect_to_chat(options):
    reader, writer = await asyncio.open_connection(
        options.host, options.port)

    while True:
        chat_message = await asyncio.wait_for(read_message(reader, logger), 10)
        async with aiofiles.open(options.history, mode='a', encoding='utf-8') as file:
            await file.write(chat_message)


if __name__ == '__main__':
    logger = setup_logger('listener')
    options = get_application_options()
    asyncio.run(connect_to_chat(options))