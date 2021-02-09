import asyncio

from utils import setup_logger, read_message, send_message, get_application_options, handle_errors


@handle_errors
async def connect_to_chat(options):
    reader, writer = await asyncio.open_connection(
        options.host, 5050)

    await asyncio.wait_for(read_message(reader, logger), 10)
    await asyncio.wait_for(send_message(writer, logger, hash), 10)
    await asyncio.wait_for(send_message(writer, logger, 'THIS IS A TEST MESSAGE, LADIES!'), 10)
    await asyncio.sleep(1)


if __name__ == '__main__':
    logger = setup_logger('sender')

    hash = '698b2744-6a16-11eb-8c47-0242ac110002'
    options = get_application_options()
    asyncio.run(connect_to_chat(options))
