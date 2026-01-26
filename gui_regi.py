import asyncio
import tkinter as tk
import tkinter.messagebox as mb
import os
from dotenv import load_dotenv
import asyncio
import threading

from write_chat import register_account


def start():
    
    load_dotenv()
    host = os.getenv('HOST')
    port = os.getenv('PORT_TO_WRITE')
    
    nick = entry.get()
    if not nick: 
        return
    
    def task():
        try:
            result = asyncio.run(register_account(nick, host, port))
            mb.showinfo("OK", f"Ник: {nick} \n Токен: {result.get('account_hash')}")
        except Exception as e:
            mb.showerror("Ошибка", str(e))
    threading.Thread(target=task, daemon=True).start()



root = tk.Tk()
root.title("Регистрация")
tk.Label(root, text="Nickname:").pack()
entry = tk.Entry(root, width=30)
entry.pack()
tk.Button(root, text="Отправить", command=start).pack()
root.mainloop()