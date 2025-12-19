
import asyncio
import datetime

import aiofiles

from arg_parser import add_cli_options

cmd_args = add_cli_options()

# "10209158-dc35-11f0-a5a4-0242ac110003"

async def write_chat():
    reader, writer = await asyncio.open_connection(
        cmd_args.host, port=5050)     
    
    greeting = await reader.read(400) # Hello %username%! Enter your personal hash or leave it empty to create new account.
    print(f"{greeting.decode()}")    
    
    hash = "10209158-dc35-11f0-a5a4-0242ac110003\n"  # 10209158-dc35-11f0-a5a4-0242ac110003
    writer.write(hash.encode('utf-8'))
    await writer.drain()  
    print(f"{hash.strip()}") # выводим в терминал или нет
 
    greeting_next = await reader.read(400) # {"nickname": "Goofy mvz", "account_hash": "10209158-dc35-11f0-a5a4-0242ac110003"}
    greeting_message = greeting_next.decode()     #Welcome to chat! Post your message below. End it with an empty line.
    print(greeting_message)
    
  
    current_data = datetime.datetime.now()
    timestamp = int(current_data.timestamp())
    date = datetime.datetime.fromtimestamp(timestamp)
    now_strftime = date.strftime('%a %d %b %Y, %I:%M%p')
    
    message = f"[{now_strftime}] mvz: Мое тестовое сообщение"
    writer.write(message.encode("utf-8"))
    await writer.drain()
    print(message.strip())
    
 
    

        
        
    
        