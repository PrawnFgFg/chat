
import asyncio
import aiofiles
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv()

from arg_parser import add_cli_options
from utils import get_current_time

HASH_TOKEN = os.getenv("HASH_TOKEN")
PORT_TO_WRITE = os.getenv("PORT_TO_WRITE")

cmd_args = add_cli_options()

now_time = get_current_time()

async def authorise(token: str = HASH_TOKEN):
    
    reader, writer = await asyncio.open_connection(host=cmd_args.host, port=PORT_TO_WRITE)
    
    # token = "89890a60-e005-11f0-a5a4-0242ac1100031"
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
        
        writer.write(f"{token}\n".encode())
        await writer.drain()
        
        account_info: bytes = await reader.readline()
        account_data: dict = json.loads(account_info.decode().strip())
        
        if not account_data:
            print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
            return
        
        welcome_to_chat = await reader.readline()
        print(welcome_to_chat.decode().strip())
        
        message = f"{account_data.get('nickname')}: Мое тестовое сообщение"
        writer.write(message.encode("utf-8"))
        await writer.drain()
        print(f'[{now_time}] {message}'.strip())
        
        
    except Exception as e:
        print(f"Error during connection: {e}")
        raise

        
 
async def register(nickname):
    
    reader, writer = await asyncio.open_connection(host=cmd_args.host, port=PORT_TO_WRITE)
    
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
                
        writer.write("\n".encode())
        await writer.drain()
        
        enter_your_nickname = await reader.readline()
        logging.info(enter_your_nickname.decode().strip())
        
        writer.write(f"{nickname}\n".encode())
        await writer.drain()
                
        new_account_info = await reader.readline()
        logging.info(new_account_info.decode().strip())
        new_account_data: dict = json.loads(new_account_info.decode().strip())
        nickname = new_account_data.get("nickname")
        
        with open('./bd_accounts_hash.json', "w", encoding="utf-8") as file:
            json.dump(new_account_data, file, indent=4)
        
        return writer, nickname
    
    except Exception as e:
        print(f"Error during connection: {e}")
        raise


async def submit_message(writer, nickname: str, message: str):
    writer.write(message.encode())
    await writer.drain()
    print(f'[{now_time}] {nickname} {message}'.strip())
    
        
    
        