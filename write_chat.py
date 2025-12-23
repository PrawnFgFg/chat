
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

async def write_chat(nickname: str = "No_name", token: str = HASH_TOKEN):
    
    reader, writer = await asyncio.open_connection(host=cmd_args.host, port=PORT_TO_WRITE)
    
    token = "ba66820e-dffe-11f0-a5a4-0242ac11000321111"
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
        
        writer.write(f"{token}\n".encode())
        await writer.drain()
        
        account_info: bytes = await reader.readline()
        account_data: dict = json.loads(account_info.decode().strip())
        if not account_data:
            print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
            
            create_new_name = await reader.readline()
            logging.info(create_new_name.decode().strip())
            
            writer.write(f"{nickname}\n".encode())
            await writer.drain()
            
            new_account_info = await reader.readline()
            logging.info(new_account_info.decode().strip())
            new_account_data: dict = json.loads(new_account_info.decode().strip())
            
            new_account_hash = new_account_data.get("account_hash")
            
            writer.close()
            await writer.wait_closed()
            
            await create_new_user(new_account_hash, new_account_data)
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
    
    finally:
        writer.close()
        await writer.wait_closed()
        
 
async def create_new_user(new_account_hash, new_account_data):
    new_reader, new_writer = await asyncio.open_connection(host=cmd_args.host, port=PORT_TO_WRITE)
    welcome2 = await new_reader.readline()
    logging.info(welcome2.decode().strip())
    
  
    
    new_writer.write(f"{new_account_hash}\n".encode())
    await new_writer.drain()
    
    welcome_to_chat2 = await new_reader.readline()
    logging.info(welcome_to_chat2.decode().strip())
    
    message2 = f"{new_account_data.get('nickname')}: Моё новое тест сообщение с нового аккаунта"
    new_writer.write(message2.encode("utf-8"))
    await new_writer.drain()
    print(f'[{now_time}] {message2}'.strip())


        
    
        