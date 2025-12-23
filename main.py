import asyncio
# import aiofiles
import logging

from arg_parser import add_cli_options
from read_chat import read_chat
from write_chat import register, submit_message

logging.basicConfig(level=logging.INFO)

cmd_args = add_cli_options()

async def main():
    
    new_user = await register("Jacky") 
    await submit_message(new_user[0], new_user[1], "Hi, I`m new")

  
if __name__ == "__main__":
    asyncio.run(main())
    
