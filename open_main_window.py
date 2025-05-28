from functools import partial
from tkinter import Label, Entry, Button, StringVar, Frame, BOTH, Y
from register import register, reset_form
from dbfunc import fetch_student_data  


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

    def open_student_register_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for student registration
        student_name_var = StringVar()
        student_birthday_var = StringVar()
        student_phone_var = StringVar()
        student_email_var = StringVar()
        student_address_var = StringVar()
        student_class_var = StringVar()

        # Add widgets to the right frame for student registration
        Label(right_frame, text="Register New Student", bg="darkblue", fg="white", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

    
        Label(right_frame, text="Student Name:", bg="darkblue", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        student_name_entry = Entry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Birthday:", bg="darkblue", fg="white").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        student_birthday_entry = Entry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=2, column=3, padx=5, pady=5)

       
        Label(right_frame, text="Student Phone:", bg="darkblue", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        student_phone_entry = Entry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Email:", bg="darkblue", fg="white").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        student_email_entry = Entry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=4, column=3, padx=5, pady=5)

       
        Label(right_frame, text="Student Address:", bg="darkblue", fg="white").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        student_address_entry = Entry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=6, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Class:", bg="darkblue", fg="white").grid(row=6, column=2, padx=5, pady=5, sticky="w")
        student_class_entry = Entry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=6, column=3, padx=5, pady=5)

        
        register_button = Button(right_frame, text="Register Student", command=partial(), bg="green", fg="black")
        register_button.grid(row=16, column=0, columnspan=8, pady=10)


        reset_button = Button(right_frame, text="Reset", command=partial(reset_form, student_name_entry, student_birthday_entry, student_phone_entry, student_email_entry, student_address_entry, student_class_entry), bg="red", fg="black")
        reset_button.grid(row=17, column=4, columnspan=8, pady=10)
        

    def open_usi_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for updating student information
        student_id_var = StringVar()
        student_name_var = StringVar()
        student_birthday_var = StringVar()
        student_phone_var = StringVar()
        student_email_var = StringVar()
        student_address_var = StringVar()
        student_class_var = StringVar()

        def populate_entries():
            """Fetch data and populate the entries."""
            student_id = student_id_var.get()
            student_data = fetch_student_data(student_id)  # Call the function from dbfunc.py

            if student_data:
                student_name_var.set(student_data["name"])
                student_birthday_var.set(student_data["birthday"])
                student_phone_var.set(student_data["phone"])
                student_email_var.set(student_data["email"])
                student_address_var.set(student_data["address"])
                student_class_var.set(student_data["class"])

        # Add widgets to the right frame for updating student information
        Label(right_frame, text="Update Student Information", bg="darkblue", fg="white", font=("Arial", 16)).grid(row=0, column=1, columnspan=8, pady=10)

        Label(right_frame, text="Student ID:", bg="darkblue", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        student_id_entry = Entry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        fetch_button = Button(right_frame, text="Fetch Data", command=populate_entries, bg="blue", fg="white")
        fetch_button.grid(row=2, column=2, padx=5, pady=5)

        Label(right_frame, text="Student Name:", bg="darkblue", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        student_name_entry = Entry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Birthday:", bg="darkblue", fg="white").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        student_birthday_entry = Entry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=4, column=3, padx=5, pady=5)

        Label(right_frame, text="Student Phone:", bg="darkblue", fg="white").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        student_phone_entry = Entry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=6, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Email:", bg="darkblue", fg="white").grid(row=6, column=2, padx=5, pady=5, sticky="w")
        student_email_entry = Entry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=6, column=3, padx=5, pady=5)

        Label(right_frame, text="Student Address:", bg="darkblue", fg="white").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        student_address_entry = Entry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=8, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Class:", bg="darkblue", fg="white").grid(row=8, column=2, padx=5, pady=5, sticky="w")
        student_class_entry = Entry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=8, column=3, padx=5, pady=5)



        register_button = Button(right_frame, text="Update Student Information", command=partial(), bg="green", fg="black")
        register_button.grid(row=16, column=0, columnspan=8, pady=10)


        reset_button = Button(right_frame, text="Reset", command=partial(reset_form, student_name_entry, student_birthday_entry, student_phone_entry, student_email_entry, student_address_entry, student_class_entry), bg="red", fg="black")
        reset_button.grid(row=17, column=4, columnspan=8, pady=10)

    def open_usg_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        student_id_var = StringVar()
        student_grade1_var = StringVar()
        student_grade2_var = StringVar()


        Label(right_frame, text="Update Student Grades", bg="darkblue", fg="white", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        Label(right_frame, text="Student ID:", bg="darkblue", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        student_id_entry = Entry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(right_frame, text="Grade 1:", bg="darkblue", fg="white").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        student_grade1_entry = Entry(right_frame, textvariable=student_grade1_var)
        student_grade1_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(right_frame, text="Grade 2:", bg="darkblue", fg="white").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        student_grade2_entry = Entry(right_frame, textvariable=student_grade2_var)
        student_grade2_entry.grid(row=6, column=1, padx=5, pady=5)



        register_button = Button(right_frame, text="Update Student Grades", command=partial(), bg="green", fg="black")
        register_button.grid(row=16, column=0, columnspan=8, pady=10)


        reset_button = Button(right_frame, text="Reset", command=partial(reset_form, student_id_entry, student_grade1_entry, student_grade2_entry), bg="red", fg="black")
        reset_button.grid(row=17, column=4, columnspan=8, pady=10)

    def open_vafs_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()





    # Add buttons to the left frame
    RegButton = Button(left_frame, text="Register New User", command=open_register_window)
    RegButton.pack(pady=10)

    SecondButton = Button(left_frame, text="Register New Student", command=open_student_register_window)
    SecondButton.pack(pady=10)

    ThirdButton = Button(left_frame, text="Update Student Information", command=open_usi_window)
    ThirdButton.pack(pady=10)

    FourthButton = Button(left_frame, text="Update Student Grades", command=open_usg_window)
    FourthButton.pack(pady=10)

    FifthButton = Button(left_frame, text="View A/F Students", command=open_vafs_window)
    FifthButton.pack(pady=10)

    ExitButton = Button(left_frame, text="Close", command=root.quit)
    ExitButton.pack(pady=10)



