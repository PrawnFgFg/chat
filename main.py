import asyncio
import aiofiles
import datetime

from arg_parser import add_cli_options
from read_chat import read_chat
from write_chat import write_chat

cmd_args = add_cli_options()

async def main():
    
    task_1 = asyncio.create_task(read_chat())
    task_2 = asyncio.create_task(write_chat())
    
    await task_1
    await task_2        
  
if __name__ == "__main__":
    asyncio.run(main())
    
