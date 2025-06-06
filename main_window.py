from functools import partial
from tkinter import Label, Entry, Button, StringVar, Frame, BOTH, Y
from MwFunc import register, populate_entries, cad_aluno, update_aluno, update_notas, pop_notas
import customtkinter as ctk
from resetforms import reset_form, reset_form2, reset_form3, reset_form4
from close import on_closing



def open_main_window(root):
    # Destroy all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the root window for the main window
    root.geometry("800x600")
    root.resizable(False, False)
    root.title("Main Window")

    # Create the left frame
    left_frame = ctk.CTkFrame(root, fg_color="#202020", width=180)
    left_frame.pack(side="left", fill=Y)
    left_frame.pack_propagate(False)

    # Create the right frame
    right_frame = ctk.CTkFrame(root, fg_color="#282828")
    right_frame.pack(side="left", fill=BOTH, expand=True)

    # Function to open the register form in the right frame
    def open_register_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for username and password
        username_var = StringVar()
        password_var = StringVar()


        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=2)

        # Add widgets to the right frame
        Label(right_frame, text="Register New User", bg="#282828", fg="white", font=("Arial", 16), anchor='center').grid(row=0, column=0, columnspan=4, pady=(10,30) ,sticky="ew")
        SuccessLabel = Label(right_frame, bg="#282828", fg="white")
        SuccessLabel.grid(row=1, column=0, columnspan=4, pady=(0,10), sticky="ew")

        SuccessLabel = Label(right_frame, bg="#282828", fg="white")
        SuccessLabel.grid(row=1, column=2, pady=(0,10), sticky="w")

        Label(right_frame, text="Username:", bg="#282828", fg="white", font=("Arial",13)).grid(row=2, column=2, pady=(5,0), sticky="w")  
        username_entry = ctk.CTkEntry(right_frame, textvariable=username_var, width=180)
        username_entry.grid(row=3, column=2, pady=(0,10), sticky="w")  

        Label(right_frame, text="Password:", bg="#282828", fg="white", font=("Arial", 13)).grid(row=4, column=2, pady=(5,0), sticky="w")
        password_entry = ctk.CTkEntry(right_frame, textvariable=password_var, show="*", width=180)
        password_entry.grid(row=5, column=2, pady=(0,10), sticky="w")  

        register_button = ctk.CTkButton(right_frame, text="Register", command=partial(register, username_var, password_var, SuccessLabel),fg_color="green", hover_color="#006400", width=180)
        register_button.grid(row=6, column=2, pady=(20,5), sticky="w")

        reset_button = ctk.CTkButton(right_frame, text="Reset",  command=partial(reset_form, username_var, password_var), fg_color="red", hover_color="#8B0000", width=180)
        reset_button.grid(row=7, column=2, pady=5, sticky="w")

    def open_student_register_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for student registration
        student_name_var = StringVar() #no banco está NOME
        student_birthday_var = StringVar()#no banco está DATA_NASCIMENTO
        student_phone_var = StringVar()#no banco está TELEFONE
        student_email_var = StringVar()#no banco está EMAIL
        student_address_var = StringVar()#no banco está ENDEREÇO
        student_class_var = StringVar()#no banco está CURSO

        # Configura a coluna para ocupar todo o espaço disponível
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)
            
        # Add widgets to the right frame for student registration
        Label(right_frame, text="Registro de novo aluno", bg="#282828", fg="white", font=("Arial", 16), anchor='center').grid(row=0, column=0, columnspan=4, pady=(10, 30), sticky="ew")
        SuccessLabel = Label(right_frame, text="", bg="#282828", fg="white")
        SuccessLabel.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

    
        Label(right_frame, text="Nome do Aluno:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=2, column=0, padx=(5,2), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=2, column=1, padx=(2,5), pady=5, sticky="w")

        Label(right_frame, text="Data de Nascimento:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=2, column=2, padx=(5,2), pady=5, sticky="e")
        student_birthday_entry = ctk.CTkEntry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=2, column=3, padx=(2,5), pady=5, sticky="w")

       
        Label(right_frame, text="Número de Telefone:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=4, column=0, padx=(5,2), pady=5, sticky="e")
        student_phone_entry = ctk.CTkEntry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=4, column=1, padx=(2,5), pady=5, sticky="w")

        Label(right_frame, text="Email do Aluno:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=4, column=2, padx=(5,2), pady=5, sticky="e")
        student_email_entry = ctk.CTkEntry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=4, column=3, padx=(2,5), pady=5, sticky="w")

        Label(right_frame, text="Endereço do Aluno:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=0, padx=(5,2), pady=5, sticky="e")
        student_address_entry = ctk.CTkEntry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=6, column=1, padx=(2,5), pady=5, sticky="w")

        Label(right_frame, text="Turma do aluno:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=2, padx=(5,2), pady=5, sticky="e")
        student_class_entry = ctk.CTkEntry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=6, column=3, padx=(2,5), pady=5, sticky="w")


        register_student_button = ctk.CTkButton(right_frame, text="Cadastrar Aluno",command=partial(cad_aluno, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel), fg_color="green", hover_color="#006400")
        register_student_button.grid(row=10, column=2, padx=(2, 5), pady=(30, 5), sticky="w")


        reset_stu_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form2, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var),  fg_color="red", hover_color="#8B0000")
        reset_stu_button.grid(row=10, column=3, padx=(2, 5), pady=(30, 5), sticky="w")
        

    def open_usi_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create StringVars for updating student information
        student_id_var = StringVar() #no banco está id
        student_name_var = StringVar() #no banco está NOME
        student_birthday_var = StringVar()#no banco está DATA_NASCIMENTO
        student_phone_var = StringVar()#no banco está TELEFONE
        student_email_var = StringVar()#no banco está EMAIL
        student_address_var = StringVar()#no banco está ENDEREÇO
        student_class_var = StringVar()#no banco está CURSO

       # Configura a coluna para ocupar todo o espaço disponível
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)
        

        # Add widgets to the right frame for updating student information
        Label(right_frame, text="Update Student Information", bg="#282828", fg="white", font=("Arial", 16), anchor='center').grid(row=0, column=0, columnspan=4, pady=(10, 30), sticky="ew")
        SuccessLabel = Label(right_frame, text="", bg="#282828", fg="white")
        SuccessLabel.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        Label(right_frame, text="Student ID:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=2, column=0, padx=(5,2), pady=5, sticky="e")
        student_id_entry = ctk.CTkEntry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        fetch_button = Button(right_frame, text="Fetch Data", command=partial(populate_entries, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel), bg="blue", fg="white")
        fetch_button.grid(row=2, column=2, padx=5, pady=5)

        Label(right_frame, text="Student Name:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=4, column=0, padx=(10,5), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Birthday:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=4, column=2,  padx=10, pady=5, sticky="ew")
        student_birthday_entry = ctk.CTkEntry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        Label(right_frame, text="Student Phone:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        student_phone_entry = ctk.CTkEntry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=6, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Email:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=2, padx=10, pady=5, sticky="ew")
        student_email_entry = ctk.CTkEntry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew")

        Label(right_frame, text="Student Address:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        student_address_entry = ctk.CTkEntry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=8, column=1, padx=5, pady=5)

        Label(right_frame, text="Student Class:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=8, column=2, padx=10, pady=5, sticky="ew")
        student_class_entry = ctk.CTkEntry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=8, column=3, padx=10, pady=5, sticky="ew")



        register_button = ctk.CTkButton(right_frame, text="Atualizar informações",command=partial(update_aluno, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel), fg_color="green", hover_color="#006400")
        register_button.grid(row=10, column=2, padx=(2,5), pady=(30, 5), sticky="w")


        reset_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form3, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var), fg_color="red", hover_color="#8B0000")
        reset_button.grid(row=10, column=3, padx=(2,5), pady=(30, 5), sticky="w")

    def open_usg_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        student_id_var = StringVar()
        student_name_var = StringVar()
        student_grade1_var = StringVar()
        student_grade2_var = StringVar()


        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)
        

        Label(right_frame, text="Atualizar as notas do Aluno", bg="#282828", fg="white", font=("Arial", 16), anchor='center').grid(row=0, column=0, pady=(10,30), sticky="ew", columnspan=4)
        SuccessLabel = Label(right_frame, text="", bg="#282828", fg="white")
        SuccessLabel.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        Label(right_frame, text="ID do aluno:", bg="#282828", fg="white", font=("Arial",10), anchor="e").grid(row=2, column=0, padx=(5,2), pady=5, sticky="e")
        student_id_entry = ctk.CTkEntry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        fetch_button = Button(right_frame, text="Buscar Dados", command=partial(pop_notas, student_id_var, student_name_var,student_grade1_var, student_grade2_var, SuccessLabel), bg="blue", fg="white")
        fetch_button.grid(row=2, column=2, padx=5, pady=5)

        Label(right_frame, text="Nome do aluno:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=4, column=0, padx=(5,2), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var, state="readonly")
        student_name_entry.grid(row=4, column=1, padx=5, pady=5)

        Label(right_frame, text="Nota 1:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=0, padx=(5,2), pady=5, sticky="e")
        student_grade1_entry = ctk.CTkEntry(right_frame, textvariable=student_grade1_var)
        student_grade1_entry.grid(row=6, column=1, padx=5, pady=5)

        Label(right_frame, text="Nota 2:", bg="#282828", fg="white", font=("Arial", 10), anchor="e").grid(row=6, column=2, padx=10, pady=5, sticky="ew")
        student_grade2_entry = ctk.CTkEntry(right_frame, textvariable=student_grade2_var)
        student_grade2_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew")


        register_button = ctk.CTkButton(right_frame, text="Update Student Grades", command=partial(update_notas, student_id_var, student_name_var,student_grade1_var, student_grade2_var, SuccessLabel) , fg_color="green", hover_color="#006400")
        register_button.grid(row=10, column=2, padx=(2,5), pady=(30, 5), sticky="w")


        reset_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form4, student_id_var, student_name_var, student_grade1_var, student_grade2_var), fg_color="red", hover_color="#8B0000")
        reset_button.grid(row=10, column=3, padx=(2,5), pady=(30, 5), sticky="w")

    def open_vafs_window():
        # Clear the right frame
        for widget in right_frame.winfo_children():
            widget.destroy()


        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)

        Label(right_frame, text="Alunos Aprovados e Reprovados", bg="#282828", fg="white", font=("Arial", 16), anchor='center').grid(row=0, column=0, pady=(10,30), sticky="ew", columnspan=4)
        SuccessLabel = Label(right_frame, text="", bg="#282828", fg="white")

        ambos_button= ctk.CTkButton(right_frame, text="Ambos", fg_color="gray")
        ambos_button.grid(row=2, column= 0, columnspan=2, padx=(5,2), pady=5, sticky="ew")
        aprovados_button = ctk.CTkButton(right_frame, text="Aprovados", fg_color="green")
        aprovados_button.grid(row=2, column= 2, columnspan=2, padx=(5,2), pady=5, sticky="ew")
        reprovados_button = ctk.CTkButton(right_frame, text="Reprovados", fg_color="red")
        reprovados_button.grid(row=2, column= 4, columnspan=2, padx=(5,2), pady=5, sticky="ew")






    # Add buttons to the left frame #202020
    RegButton = ctk.CTkButton(left_frame, text="Register New User", command=open_register_window, fg_color="#202020")
    RegButton.pack(pady=10)

    SecondButton = ctk.CTkButton(left_frame, text="Register New Student", command=open_student_register_window, fg_color="#202020")
    SecondButton.pack(pady=10)

    ThirdButton = ctk.CTkButton(left_frame, text="Update Student Information", command=open_usi_window, fg_color="#202020")
    ThirdButton.pack(pady=10)

    FourthButton = ctk.CTkButton(left_frame, text="Atualizar notas do Aluno", command=open_usg_window, fg_color="#202020")
    FourthButton.pack(pady=10)

    FifthButton = ctk.CTkButton(left_frame, text="View A/F Students", command=open_vafs_window, fg_color="#202020")
    FifthButton.pack(pady=10)

    ExitButton = ctk.CTkButton(left_frame, text="Close", command=lambda: on_closing(root), fg_color="#202020")
    ExitButton.pack(pady=10)



