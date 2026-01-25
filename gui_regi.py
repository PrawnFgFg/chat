# import asyncio
# import tkinter as tk

# from write_chat import register_account


# async def get_token(root, host, port_to_write, registration_queue):
    
#     registation_frame = tk.Toplevel(root)
#     registation_frame.title("Регистрация")
#     registation_frame.geometry("300x200")
#     registation_frame.transient(root)  
#     registation_frame.grab_set()  
    
#     lable_input_name = tk.Label(registation_frame, text="Введите nickname")
#     lable_input_name.pack()
    
#     ent_nick = tk.Entry(registation_frame)
#     ent_nick.pack()
    
#     def get_nick():
#         nickname = ent_nick.get()
#         result_label.config(text=f"Ваш ник: {nickname}")
#         registration_queue.put_nowait(nickname)
    
#     but_nick = tk.Button(registation_frame, text="Отправить", command=get_nick)
#     but_nick.pack()
    
    
#     result_label = tk.Label(registation_frame, text="")
#     result_label.pack()
  
    
    
    
        
    
    
        
        
        
#     # async def button_registration():
#         # account_data: dict = await register_account(
#         #     nickname="nickname",
#         #     host=host,
#         #     port_to_write=port_to_write,
#         # )
        
#     # but_nick.bind('<Button-1>', get_nick)
#     # account_hash = account_data.get("accoutn_hash") 
    
    
#     # registration_queue.put_nowait(nick)
        