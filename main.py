import asyncio
from time import strftime
import aiofiles
import datetime

from arg_parser import add_cli_options

host, port, path_file_history = add_cli_options()

#formatted_date_3 = now.strftime("%Y-%m-%d-%H.%M.%S")
async def mine_chat():
    reader, writer = await asyncio.open_connection(
        host, port)

    while True:
        current_data = datetime.datetime.now()
        timestamp = int(current_data.timestamp())
        date = datetime.datetime.fromtimestamp(timestamp)
        now_strftime = date.strftime('%a %d %b %Y, %I:%M%p')
        
        data_chat = await reader.read(200)
        new_message = f'[{now_strftime}] {data_chat.decode()}\n'
        
        async with aiofiles.open(path_file_history, "a", encoding='utf-8') as file:
            await file.write(new_message)
        
        print(new_message)


asyncio.run(mine_chat())