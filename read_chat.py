import asyncio
import aiofiles
import logging
import time

from async_timeout import timeout

from gui_models import ReadConnectionStateChanged
from utils import get_current_time

async def read_chat(
    host, 
    port, 
    queue_status, 
    path_history: str | None = None, 
    print_to_console=False, 
    queue: asyncio.Queue | None = None,
    watchdog_queue: asyncio.Queue | None = None,
):
    now_time = get_current_time()
    
    timestamp = int(time.time())
    reader = None
    writer = None
    
    
    queue_status.put_nowait(ReadConnectionStateChanged.INITIATED)
    await asyncio.sleep(1)
    
    try:
        while True:
            
            if not reader and not writer:
                reader, writer = await asyncio.open_connection(
                host=host, port=port)
                
            if reader:
                queue_status.put_nowait(ReadConnectionStateChanged.ESTABLISHED)
                
            data_chat = await reader.read(200)
            new_message = f'[{now_time}] {data_chat.decode()}\n'
            
            if queue and not path_history:
                queue.put_nowait(new_message.strip())
                watchdog_queue.put_nowait(f"[{timestamp}] Connection is alive. New message in chat")
                logging.info(new_message)
                
            if path_history:
                async with aiofiles.open(path_history, "a", encoding='utf-8') as file:
                    await file.write(new_message)
                
            if print_to_console:
                print(new_message.strip())
                
                
    except UnicodeDecodeError:
        logging.info(f"[{now_time}] Попытка декодировать неполные байты как UTF-8 после обрыва соединения")
            
    
    finally:
        queue_status.put_nowait(ReadConnectionStateChanged.CLOSED)
        writer.close()
        await writer.wait_closed()
        
        
        
async def read_msgs(host, port, queue, queue_status, watchdog_queue, path_history=None):
    await read_chat(
        host=host,
        port=port,
        queue_status=queue_status,
        path_history=path_history,
        queue=queue,
        watchdog_queue=watchdog_queue
    )
        
        
async def watch_for_connection(watchdog_queue: asyncio.Queue):
    
    timestamp = int(time.time())
    
    while True:
        timestamp = int(time.time())
        try:
            async with timeout(10) as cm:    
                watchdog_queue_message = await watchdog_queue.get()
                print(watchdog_queue_message)
        except TimeoutError:
            if cm.expired() is True:
                print(f"[{timestamp}] 10s timeout is elapsed")
                raise ConnectionError

        
     
      
            
        