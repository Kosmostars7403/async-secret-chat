import asyncio

from utils import setup_logger, read_message, submit_message, get_application_options, handle_errors, register, \
    authorize


@handle_errors
async def connect_to_chat(options):
    reader, writer = await connect_for_authorize(options.host, port)

    if username:
        token = await asyncio.wait_for(register(writer, reader, logger, username), 10)

        reader, writer = await connect_for_authorize(options.host, port)

        await authorize(writer, reader, token, logger)
        await asyncio.wait_for(submit_message(writer, logger, message), 10)
    else:
        nickname = await authorize(writer, reader, hash, logger)
        if not nickname:
            return
        await asyncio.wait_for(submit_message(writer, logger, message), 10)


@handle_errors
async def connect_for_authorize(host, port):
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(host, port),
        10
    )

    server_start_message = await asyncio.wait_for(read_message(reader), 10)
    logger.debug(server_start_message)

    return reader, writer


if __name__ == '__main__':
    logger = setup_logger('sender')
    username = ''
    message = 'THIS IS A TEST MESSAGE, LADIES!'
    port = 5050
    hash = '698b2744-6a16-11eb-8c47-0242ac110002'
    options = get_application_options()
    asyncio.run(connect_to_chat(options))
