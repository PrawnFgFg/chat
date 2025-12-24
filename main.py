import asyncio
import logging

from arg_parser import add_cli_options
from read_chat import read_chat
from write_chat import register, submit_message, authorise

logging.basicConfig(level=logging.INFO)

cmd_args = add_cli_options()

async def main():
    
    # new_user = await register("Jacky") 
    
    user = await authorise()
    await submit_message(user[0], user[1])
    await read_chat()
    

  
if __name__ == "__main__":
    asyncio.run(main())
    
