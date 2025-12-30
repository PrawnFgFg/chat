import asyncio
import logging
import json

from utils import get_current_time

async def authorise(port_to_write: int, cmd_args: str):
    
    reader, writer = await asyncio.open_connection(host=cmd_args.host, port=port_to_write)
    
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
        
        writer.write(f"{cmd_args.token}\n".encode())
        await writer.drain()
        
        account_info: bytes = await reader.readline()
        account_data: dict = json.loads(account_info.decode().strip())
        nickname = account_data.get("nickname")
        
        if not account_data:
            print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
            return
        
        welcome_to_chat = await reader.readline()
        print(welcome_to_chat.decode().strip())
        
        return writer, nickname
        
        
    except Exception as e:
        print(f"Error during connection: {e}")
        raise
    
    except asyncio.CancelledError:
        print("Работа завершена")
        
        
 
async def register(nickname, cmd_args, port_to_write):
    
    reader, writer = await asyncio.open_connection(host=cmd_args.host, port=port_to_write)
    
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
        
        with open('./bd_accounts_hash.json', "a", encoding="utf-8") as file:
            json.dump(new_account_data, file, indent=4)
        
        await submit_message(writer, nickname)
        
        return writer, nickname
    
    except Exception as e:
        print(f"Error during connection: {e}")
        raise
    
    except asyncio.CancelledError:
        print("Работа завершена")
        


async def submit_message(writer, nickname: str, cmd_args):
    now_time = get_current_time()
    writer.write(cmd_args.message.encode())
    await writer.drain()
    print(f'[{now_time}] {nickname}: {cmd_args.message}'.strip())
    
        
    
        