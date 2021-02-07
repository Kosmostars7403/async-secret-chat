import asyncio


async def connect_to_chat(message):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        chat_message = await reader.read(100)
        print(chat_message.decode())


if __name__ == '__main__':
    asyncio.run(connect_to_chat('Hello World!'))