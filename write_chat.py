import asyncio
import logging
import json
import time
from socket import gaierror

from tkinter import messagebox

from async_timeout import timeout
from gui_models import NicknameReceived, SendingConnectionStateChanged
from utils import get_current_time

from read_chat import read_chat
from exceptions import InvalidTokenException

async def authorise(
    port_to_write: int, 
    host: str, 
    token, 
    queue, 
    queue_status,
    watchdog_queue,
):
    
    timestamp = int(time.time())
    
    reader, writer = await asyncio.open_connection(host, port=port_to_write)
    
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
        
        watchdog_queue.put_nowait(f'[{timestamp}] Connection is alive. Prompt before auth')
        
        writer.write(f"{token}\n".encode())
        await writer.drain()
        
        account_info: bytes = await reader.readline()
        account_data: dict = json.loads(account_info.decode().strip())
        
        if account_data is None:
            messagebox.showinfo("Invalid token", "Проверьте тоекн. Сервер его не узнал")
            raise InvalidTokenException
        
        nickname = account_data.get("nickname")
        
        if not account_data:
            print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
            return
        
        welcome_to_chat = await reader.readline()
        logging.info(welcome_to_chat.decode().strip())
        
        print(f'Выполнена авторизация. Пользователь {nickname}')
        event_nickname = NicknameReceived(nickname)
        
        if event_nickname:
            watchdog_queue.put_nowait(f'[{timestamp}] Connection is alive. Authorization done')
            
        queue_status.put_nowait(event_nickname)
        
        return reader, writer
    
    except gaierror:
        print("Ошибка gaierrror")
    
    except Exception as e:
        print(f"Error during connection in writer: {e}")
        raise
    
    except asyncio.CancelledError:
        print("Работа завершена в writer")
        
        
 
async def register_account(
    nickname, 
    host, 
    port_to_write,
    queue,
    queue_status,
    watchdog_queue,
):
    timestamp = int(time.time())
    
    reader, writer = await asyncio.open_connection(host=host, port=port_to_write)
    
    try:
        welcome = await reader.readline()
        logging.info(welcome.decode().strip())
        
        watchdog_queue.put_nowait(f'[{timestamp}] Connection is alive. Prompt before auth')
                
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
        
        event_nickname = NicknameReceived(nickname)
        
        if event_nickname:
            watchdog_queue.put_nowait(f'[{timestamp}] Connection is alive. Authorization done')
        
        queue_status.put_nowait(nickname)
        
        return new_account_data
    
    except Exception as e:
        print(f"Error during connection: {e}")
        raise
    
    except asyncio.CancelledError:
        print("Работа завершена")
        


async def submit_message(writer, nickname: str, cmd_args, queue):
    now_time = get_current_time()
    writer.write(cmd_args.message.encode())
    await writer.drain()
    await queue.get(f'[{now_time}] {nickname}: {cmd_args.message}'.strip())
    

async def save_messages(host, port, filepath, queue, queue_status):
    await read_chat(
        host=host,
        port=port,
        path_history=filepath,
        queue=queue,
        queue_status=queue_status
    )
        



async def send_msgs(host, port, queue, token, queue_status, watchdog_queue):
    timestamp = int(time.time())
    reader, writer = await authorise(
        host=host,
        port_to_write=port,
        queue=queue,
        token=token,
        queue_status=queue_status,
        watchdog_queue=watchdog_queue,
    )
    
    if writer:
        queue_status.put_nowait(SendingConnectionStateChanged.ESTABLISHED)
    
    while True:
        
        msg = await queue.get()
        writer.write(msg.encode() + b'\n\n')
        await writer.drain()
        
        if msg:
            watchdog_queue.put_nowait(f"[{timestamp}] Connection is alive. Message sent")
        
        print(f"Пользователь написал: {msg}")
        
        
async def send_empty_msg(
    host,
    port,
    watchdog_status_queue,
):
    reader, writer = await asyncio.open_connection(
            host=host, port=port)

    msg = '\n'
    
    await reader.readline() # welcome
        
    writer.write(f"\n".encode())
    await writer.drain()
    
    await reader.readline() # enter_your_nickname
    
    writer.write(f"\n".encode())
    await writer.drain()
    
    await reader.readline() #new_account_info

    while True:
        try:
            async with timeout(6) as cm:
                await asyncio.sleep(4)
                writer.write(f"{msg}\n".encode())
                await writer.drain()
                
                watchdog_status_queue.put_nowait(msg)
               
        except TimeoutError:
            if cm.expired() is True:
                print("Ошибка, сервер долго не получал пустое сообщение", cm.expired())
                raise gaierror


