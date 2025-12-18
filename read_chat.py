import asyncio
import aiofiles
import datetime

from arg_parser import add_cli_options


cmd_args = add_cli_options()

async def read_chat():
    reader, writer = await asyncio.open_connection(
        cmd_args.host, cmd_args.port)

    while True:
        current_data = datetime.datetime.now()
        timestamp = int(current_data.timestamp())
        date = datetime.datetime.fromtimestamp(timestamp)
        now_strftime = date.strftime('%a %d %b %Y, %I:%M%p')
        
        data_chat = await reader.read(200)
        new_message = f'[{now_strftime}] {data_chat.decode()}\n'
        
        
        async with aiofiles.open(cmd_args.path_history, "a", encoding='utf-8') as file:
            await file.write(new_message)
        
        print(new_message)
        