import asyncio
import logging
import os

from dotenv import load_dotenv

from arg_parser import add_cli_options
from read_chat import read_chat
from write_chat import submit_message, authorise


PORT_TO_WRITE = os.getenv("PORT_TO_WRITE")

cmd_args = add_cli_options()

logging.basicConfig(level=logging.INFO)

async def main():
    
    load_dotenv()
    
    try:
        user_writer, user_nickname = await authorise(port_to_write=PORT_TO_WRITE, cmd_args=cmd_args)
        await submit_message(user_writer, user_nickname, cmd_args)
        await read_chat(cmd_args)
        
    finally:
        user_writer.close()
    

  
if __name__ == "__main__":
    asyncio.run(main())
    
