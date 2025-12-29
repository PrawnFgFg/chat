import asyncio
import logging

from arg_parser import add_cli_options
from read_chat import read_chat
from write_chat import register, submit_message, authorise

logging.basicConfig(level=logging.INFO)

cmd_args = add_cli_options()

async def main():
    
    try:
        user_writer, user_nickname = await authorise()
        await submit_message(user_writer, user_nickname)
        await read_chat()
        
    finally:
        user_writer.close()
    

  
if __name__ == "__main__":
    asyncio.run(main())
    
