
import asyncio
import datetime

import aiofiles

from arg_parser import add_cli_options

cmd_args = add_cli_options()

# "10209158-dc35-11f0-a5a4-0242ac110003"

async def write_chat(username, text):
    reader, writer = await asyncio.open_connection(
        cmd_args.host, port=5050)
    
    username = "FgFg"
    
    current_data = datetime.datetime.now()
    timestamp = int(current_data.timestamp())
    date = datetime.datetime.fromtimestamp(timestamp)
    now_strftime = date.strftime('%a %d %b %Y, %I:%M%p')
    
    message = f"{[now_strftime]} {username}: {text}\n" 
    text = writer.write(message.encode('utf-8'))
    await writer.drain()  
    
    print(f"{message.strip()}")

    writer.close()
    await writer.wait_closed()
        
        