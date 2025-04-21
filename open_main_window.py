from functools import partial
from tkinter import Label, Entry, Button, StringVar, Frame, BOTH, Y
from register import register, reset_form


def open_main_window(root):
    # Destroy all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the root window for the main window
    root.geometry("800x600")
    root.resizable(False, False)
    root.title("Main Window")

    # Create the left frame
    left_frame = Frame(root, bg="lightblue", width=160)
    left_frame.pack(side="left", fill=Y)
    left_frame.pack_propagate(False)

    # Create the right frame
    right_frame = Frame(root, bg="darkblue")
    right_frame.pack(side="left", fill=BOTH, expand=True)

    # Function to open the register form in the right frame
    def open_register_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for username and password
        username_var = StringVar()
        password_var = StringVar()

        # Add widgets to the right frame
        Label(right_frame, text="Register New User", bg="darkblue", fg="white", font=("Arial", 16)).pack(pady=10)
        SuccessLabel = Label(right_frame, bg="darkblue", fg="white")
        SuccessLabel.pack(pady=5)
        Label(right_frame, text="Username:", bg="darkblue", fg="white").pack(pady=5)
        username_entry = Entry(right_frame, textvariable=username_var)
        username_entry.pack(pady=5)

        Label(right_frame, text="Password:", bg="darkblue", fg="white").pack(pady=5)
        password_entry = Entry(right_frame, textvariable=password_var, show="*")
        password_entry.pack(pady=5)

        
        register_button = Button(right_frame, text="Register", command=partial(register, username_entry, password_entry, SuccessLabel), bg="green", fg="black")
        register_button.pack(pady=10)

        reset_button = Button(right_frame, text="Reset", command=partial(reset_form, username_entry, password_entry), bg="red", fg="black")
        reset_button.pack(pady=10)

    # Add buttons to the left frame
    RegButton = Button(left_frame, text="Register New User", command=open_register_window)
    RegButton.pack(pady=10)

    SecondButton = Button(left_frame, text="Second Button", command=lambda: print("Second button clicked"))
    SecondButton.pack(pady=10)

    ThirdButton = Button(left_frame, text="Third Button", command=lambda: print("Third button clicked"))
    ThirdButton.pack(pady=10)

    FourthButton = Button(left_frame, text="Fourth Button", command=lambda: print("Fourth button clicked"))
    FourthButton.pack(pady=10)

    FifthButton = Button(left_frame, text="Fifth Button", command=lambda: print("Fifth button clicked"))
    FifthButton.pack(pady=10)

    ExitButton = Button(left_frame, text="Close", command=root.quit)
    ExitButton.pack(pady=10)



