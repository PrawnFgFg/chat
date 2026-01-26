import asyncio
import logging
import os

from anyio import create_task_group
from dotenv import load_dotenv

from arg_parser import add_cli_options, port_write
from gui import draw
from gui_models import TkAppClosed
from write_chat import save_messages
from main_connection import handle_connection

PORT_TO_WRITE = os.getenv("PORT_TO_WRITE")

cmd_args = add_cli_options()

logging.basicConfig(level=logging.INFO)


async def main(
    host=cmd_args.host,
    port_to_read=cmd_args.port,
    port_to_write=port_write,
    path_history=cmd_args.path_history,
    token=cmd_args.token
):
    load_dotenv()
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    try:
        async with create_task_group() as tg:
            tg.start_soon(
                draw,
                messages_queue,
                sending_queue,
                status_updates_queue)
            tg.start_soon(
                save_messages,
                host,
                port_to_read,
                path_history,
                messages_queue,
                status_updates_queue)
            tg.start_soon(
                handle_connection,
                host,
                port_to_read,
                port_to_write,
                token,
                messages_queue,
                status_updates_queue,
                watchdog_queue,
                sending_queue,
                status_updates_queue,
                )
    except ExceptionGroup as eg:
        for e in eg.exceptions:
            if isinstance(e, TkAppClosed):
                print("Завершение программы")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма корректно завершена пользователем")
