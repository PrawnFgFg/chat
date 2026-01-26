from socket import gaierror
from anyio import create_task_group

from gui_models import NicknameReceived, ReadConnectionStateChanged, SendingConnectionStateChanged
from read_chat import read_msgs, watch_for_connection
from write_chat import send_empty_msg, send_msgs


async def handle_connection(
    host,
    port_to_read,
    port_to_write,
    token,
    messages_queue,
    status_updates_queue,
    watchdog_queue,
    sending_queue,
    queue_status,
):
    while True:
        
        try:
            async with create_task_group() as tg:
                
                tg.start_soon(
                    read_msgs, 
                    host, 
                    port_to_read, 
                    messages_queue, 
                    status_updates_queue, 
                    watchdog_queue
                    )
                
                tg.start_soon(
                    send_msgs, 
                    host, 
                    port_to_write, 
                    sending_queue, 
                    token, 
                    status_updates_queue, 
                    watchdog_queue
                    )
                
                tg.start_soon(
                    watch_for_connection, 
                    watchdog_queue
                    )
                
                tg.start_soon(
                    send_empty_msg, 
                    host, 
                    port_to_write, 
                    watchdog_queue
                    )
                
        except ExceptionGroup as eg:
            for e in eg.exceptions:
                if isinstance(e, (ConnectionError, gaierror)):
                    queue_status.put_nowait(ReadConnectionStateChanged.INITIATED)
                    queue_status.put_nowait(SendingConnectionStateChanged.INITIATED)
                    event_nickname = NicknameReceived("Неизвестно")
                    queue_status.put_nowait(event_nickname)