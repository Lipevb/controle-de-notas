from tkinter import *
from functools import partial
from functions import login, register  # Import functions from functions.py

root = Tk()
root.geometry("400x300")
titlelabel = Label(root, text="Please Enter User and Password")
SuccessLabel = Label(root)

user_var = StringVar()
USER = Entry(root, textvariable=user_var)
user_var.set('Username')

pass_var = StringVar()
PASS = Entry(root, textvariable=pass_var, show="*")
pass_var.set('Password')

LogButton = Button(root, text="Login", command=partial(login, user_var, pass_var, SuccessLabel))
RegButton = Button(root, text="Register new user", command=partial(register, user_var, pass_var, SuccessLabel))

titlelabel.pack()
SuccessLabel.pack()
USER.pack()
PASS.pack()
LogButton.place(x=150, y=100, height=50, width=100)
RegButton.place(x=150, y=150, height=50, width=100)
root.title("Login")
root.mainloop()