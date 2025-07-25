from tkinter import Tk, Label, Entry, Button, StringVar
from functools import partial
from Login import login
from main_window import open_main_window 
from close import on_closing, close_all
import customtkinter as ctk
import atexit

def login_and_open_main(user_var, pass_var, success_label, root):
    username = user_var.get()
    password = pass_var.get()
    user_var.set("")
    pass_var.set("")

    if login(username, password, success_label):
        print("Login successful!")
        open_main_window(root)
    else:
        print("Login failed!")



atexit.register(close_all)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("300x250")

root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

titlelabel = ctk.CTkLabel(root, text="Insira Usuário e Senha", font=("Arial", 13 , "bold"))
SuccessLabel = ctk.CTkLabel(root, text="")

user_var = ctk.StringVar()
USER = ctk.CTkEntry(root, textvariable=user_var)
user_var.set('')

pass_var = ctk.StringVar()
PASS = ctk.CTkEntry(root, textvariable=pass_var, show="*")
pass_var.set('')

LogButton = ctk.CTkButton(root, text="Login", command=partial(login_and_open_main, user_var, pass_var, SuccessLabel, root), fg_color="green", hover_color="#006400")
ExitButton = ctk.CTkButton(root, text="Fechar", command=lambda: on_closing(root), fg_color="red", hover_color="#8B0000")

titlelabel.pack()
SuccessLabel.pack()
titlelabel.pack(pady=(10, 0))
USER.pack(pady=5)
PASS.pack(pady=5)
LogButton.pack(pady=(20,5))
ExitButton.pack(pady=5)
root.title("Login")
root.resizable(False, False)
root.mainloop()