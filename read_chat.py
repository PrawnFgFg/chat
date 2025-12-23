import asyncio
import aiofiles
import logging

from arg_parser import add_cli_options
from utils import get_current_time


cmd_args = add_cli_options()

async def read_chat():
    now_time = get_current_time()
    
    reader, writer = await asyncio.open_connection(
            cmd_args.host, cmd_args.port)
    
    try:
        while True:
            data_chat = await reader.read(200)
            new_message = f'[{now_time}] {data_chat.decode()}\n'
            
            async with aiofiles.open(cmd_args.path_history, "a", encoding='utf-8') as file:
                await file.write(new_message)
            
            print(new_message.strip())
            logging.info(new_message)
            
    except Exception as e:
        print(f"Error during connection: {e}")
        raise
    
    finally:
        writer.close()
        await writer.wait_closed()
        
   
        