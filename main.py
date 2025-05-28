from tkinter import Tk, Label, Entry, Button, StringVar
from functools import partial
from functions import login
from open_main_window import open_main_window 

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

root = Tk()
root.geometry("300x200")
titlelabel = Label(root, text="Please Enter User and Password")
SuccessLabel = Label(root)

user_var = StringVar()
USER = Entry(root, textvariable=user_var)
user_var.set('')

pass_var = StringVar()
PASS = Entry(root, textvariable=pass_var, show="*")
pass_var.set('')

LogButton = Button(root, text="Login", command=partial(login_and_open_main, user_var, pass_var, SuccessLabel, root), bg="green")
ExitButton = Button(root, text="Close", command=root.quit, bg="red")

titlelabel.pack()
SuccessLabel.pack()
USER.pack()
PASS.pack()
LogButton.place(x=100, y=100, height=25, width=100)
ExitButton.place(x=100, y=130, height=25, width=100)
root.title("Login")
root.resizable(False, False)
root.mainloop()