from functools import partial
from tkinter import StringVar, BOTH, Y
import customtkinter as ctk
from MwFunc import register, populate_entries, cad_aluno, update_aluno, update_notas, pop_notas
from resetforms import reset_form, reset_form2, reset_form3, reset_form4
from close import on_closing
from table_functions import create_table_header, populate_table, setup_table_frame_columns



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

    welcome_title = ctk.CTkLabel(
    right_frame,
    text="Seja bem-vindo(a)!",
    font=ctk.CTkFont(size=20, weight="bold"),
    justify="center"
)
    welcome_title.place(relx=0.5, rely=0.4, anchor="center")

    welcome_msg = ctk.CTkLabel(
        right_frame,
        text="Clique em algum botão na lateral esquerda para acessar o serviço desejado.",
        font=ctk.CTkFont(size=14),
        justify="center"
    )
    welcome_msg.place(relx=0.5, rely=0.48, anchor="center")

    def cleanup_right_frame():
        try:
            for widget in right_frame.winfo_children():
                try:
                    for child in widget.winfo_children():
                        child.destroy()
                    widget.destroy()
                except:
                    pass
            
            # Reset all column configurations
            for i in range(10):  # Reset first 10 columns (more than enough)
                right_frame.grid_columnconfigure(i, weight=0, minsize=0)
            
            # Reset all row configurations
            for i in range(20):
                right_frame.grid_rowconfigure(i, weight=0, minsize=0)
            

            right_frame.update_idletasks()
            
        except Exception as e:
            print(f"Error in cleanup: {e}")
    
    # Update the display
    right_frame.update()

    # Function to open the register form in the right frame
    def open_register_window():
        cleanup_right_frame()  # Use enhanced cleanup

        # Create StringVars for username and password
        username_var = StringVar()
        password_var = StringVar()


        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=2)

        # ✅ Use CustomTkinter labels consistently
        title_label = ctk.CTkLabel(right_frame, text="Registrar Novo Usuário", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(10,30), sticky="ew")
        
        success_label = ctk.CTkLabel(right_frame, text="")
        success_label.grid(row=1, column=0, columnspan=4, pady=(0,10), sticky="ew")

        username_label = ctk.CTkLabel(right_frame, text="Username:", font=ctk.CTkFont(size=13))
        username_label.grid(row=2, column=2, pady=(5,0), sticky="w")
        
        username_entry = ctk.CTkEntry(right_frame, textvariable=username_var, width=180)
        username_entry.grid(row=3, column=2, pady=(0,10), sticky="w")

        password_label = ctk.CTkLabel(right_frame, text="Password:", font=ctk.CTkFont(size=13))
        password_label.grid(row=4, column=2, pady=(5,0), sticky="w")
        
        password_entry = ctk.CTkEntry(right_frame, textvariable=password_var, show="*", width=180)
        password_entry.grid(row=5, column=2, pady=(0,10), sticky="w")

        register_button = ctk.CTkButton(right_frame, text="Registrar", command=partial(register, username_var, password_var, success_label),fg_color="green", hover_color="#006400", width=180)
        register_button.grid(row=6, column=2, pady=(20,5), sticky="w")

        reset_button = ctk.CTkButton(right_frame, text="Reset",  command=partial(reset_form, username_var, password_var), fg_color="red", hover_color="#8B0000", width=180)
        reset_button.grid(row=7, column=2, pady=5, sticky="w")

    def open_student_register_window():
        cleanup_right_frame()

        # Create StringVars for student registration
        student_name_var = StringVar() #no banco está NOME
        student_birthday_var = StringVar()#no banco está DATA_NASCIMENTO
        student_phone_var = StringVar()#no banco está TELEFONE
        student_email_var = StringVar()#no banco está EMAIL
        student_address_var = StringVar()#no banco está ENDEREÇO
        student_class_var = StringVar()#no banco está CURSO

        # Configure grid
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)

        # ✅ Use CustomTkinter labels consistently
        title_label = ctk.CTkLabel(right_frame, text="Registrar novo aluno", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(10, 30), sticky="ew")
        
        success_label = ctk.CTkLabel(right_frame, text="")
        success_label.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        # Student form fields
        ctk.CTkLabel(right_frame, text="Nome do Aluno:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=(5,2), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=3, column=1, padx=(2,5), pady=5, sticky="w")

        ctk.CTkLabel(right_frame, text="Data de Nascimento:", font=ctk.CTkFont(size=13)).grid(row=3, column=2, padx=(5,2), pady=5, sticky="e")
        student_birthday_entry = ctk.CTkEntry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=3, column=3, padx=(2,5), pady=5, sticky="w")

        ctk.CTkLabel(right_frame, text="Número de Telefone:", font=ctk.CTkFont(size=13)).grid(row=5, column=0, padx=(5,2), pady=5, sticky="e")
        student_phone_entry = ctk.CTkEntry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=5, column=1, padx=(2,5), pady=5, sticky="w")

        ctk.CTkLabel(right_frame, text="Email do Aluno:", font=ctk.CTkFont(size=13)).grid(row=5, column=2, padx=(5,2), pady=5, sticky="e")
        student_email_entry = ctk.CTkEntry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=5, column=3, padx=(2,5), pady=5, sticky="w")

        ctk.CTkLabel(right_frame, text="Endereço do Aluno:", font=ctk.CTkFont(size=13)).grid(row=7, column=0, padx=(5,2), pady=5, sticky="e")
        student_address_entry = ctk.CTkEntry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=7, column=1, padx=(2,5), pady=5, sticky="w")

        ctk.CTkLabel(right_frame, text="Turma do aluno:", font=ctk.CTkFont(size=13)).grid(row=7, column=2, padx=(5,2), pady=5, sticky="e")
        student_class_entry = ctk.CTkEntry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=7, column=3, padx=(2,5), pady=5, sticky="w")


        register_student_button = ctk.CTkButton(right_frame, text="Cadastrar Aluno",command=partial(cad_aluno, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, success_label), fg_color="green", hover_color="#006400")
        register_student_button.grid(row=10, column=2, padx=(2, 5), pady=(30, 5), sticky="w")


        reset_stu_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form2, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var),  fg_color="red", hover_color="#8B0000")
        reset_stu_button.grid(row=10, column=3, padx=(2, 5), pady=(30, 5), sticky="w")

    def open_usi_window():
        cleanup_right_frame()

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

        # ✅ Use CustomTkinter labels consistently
        title_label = ctk.CTkLabel(right_frame, text="Atualizar informação de Aluno", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(10, 30), sticky="ew")
        
        success_label = ctk.CTkLabel(right_frame, text="")
        success_label.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(right_frame, text="ID do Aluno:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=(5,2), pady=5, sticky="e")
        student_id_entry = ctk.CTkEntry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        fetch_button = ctk.CTkButton(right_frame, text="Buscar Dados", command=partial(populate_entries, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, success_label), fg_color="blue", hover_color="#0066CC")
        fetch_button.grid(row=2, column=2, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Nome do Aluno:", font=ctk.CTkFont(size=13)).grid(row=4, column=0, padx=(10,5), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var)
        student_name_entry.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Data de nascimento:", font=ctk.CTkFont(size=13)).grid(row=4, column=2,  padx=10, pady=5, sticky="ew")
        student_birthday_entry = ctk.CTkEntry(right_frame, textvariable=student_birthday_var)
        student_birthday_entry.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(right_frame, text="Número de Telefone:", font=ctk.CTkFont(size=13)).grid(row=6, column=0, padx=5, pady=5, sticky="e")
        student_phone_entry = ctk.CTkEntry(right_frame, textvariable=student_phone_var)
        student_phone_entry.grid(row=6, column=1, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Email do Aluno:", font=ctk.CTkFont(size=13)).grid(row=6, column=2, padx=10, pady=5, sticky="ew")
        student_email_entry = ctk.CTkEntry(right_frame, textvariable=student_email_var)
        student_email_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(right_frame, text="Endereço do Aluno:", font=ctk.CTkFont(size=13)).grid(row=8, column=0, padx=5, pady=5, sticky="e")
        student_address_entry = ctk.CTkEntry(right_frame, textvariable=student_address_var)
        student_address_entry.grid(row=8, column=1, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Turma do Aluno:", font=ctk.CTkFont(size=13)).grid(row=8, column=2, padx=10, pady=5, sticky="ew")
        student_class_entry = ctk.CTkEntry(right_frame, textvariable=student_class_var)
        student_class_entry.grid(row=8, column=3, padx=10, pady=5, sticky="ew")



        register_button = ctk.CTkButton(right_frame, text="Atualizar informações",command=partial(update_aluno, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, success_label), fg_color="green", hover_color="#006400")
        register_button.grid(row=10, column=2, padx=(2,5), pady=(30, 5), sticky="w")


        reset_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form3, student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var), fg_color="red", hover_color="#8B0000")
        reset_button.grid(row=10, column=3, padx=(2,5), pady=(30, 5), sticky="w")

    def open_usg_window():
        cleanup_right_frame()

        student_id_var = StringVar()
        student_name_var = StringVar()
        student_grade1_var = StringVar()
        student_grade2_var = StringVar()
        student_media_var = StringVar()

        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)

        title_label = ctk.CTkLabel(right_frame, text="Atualizar notas do Aluno", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, pady=(10,30), sticky="ew", columnspan=4)
        
        success_label = ctk.CTkLabel(right_frame, text="")
        success_label.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(right_frame, text="ID do aluno:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=(5,2), pady=5, sticky="e")
        student_id_entry = ctk.CTkEntry(right_frame, textvariable=student_id_var)
        student_id_entry.grid(row=2, column=1, padx=5, pady=5)

        fetch_button = ctk.CTkButton(right_frame, text="Buscar Dados", command=partial(pop_notas, student_id_var, student_name_var,student_grade1_var, student_grade2_var, student_media_var, success_label), fg_color="blue", hover_color="#0066CC")
        fetch_button.grid(row=2, column=2, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Nome do aluno:", font=ctk.CTkFont(size=13)).grid(row=4, column=0, padx=(5,2), pady=5, sticky="e")
        student_name_entry = ctk.CTkEntry(right_frame, textvariable=student_name_var, state="readonly")
        student_name_entry.grid(row=4, column=1, padx=5, pady=5)


        ctk.CTkLabel(right_frame, text="Nota 1:", font=ctk.CTkFont(size=13)).grid(row=6, column=0, padx=(5,2), pady=5, sticky="e")
        student_grade1_entry = ctk.CTkEntry(right_frame, textvariable=student_grade1_var, placeholder_text_color="white", placeholder_text="5.55")
        student_grade1_entry.grid(row=6, column=1, padx=5, pady=5)

        ctk.CTkLabel(right_frame, text="Nota 2:", font=ctk.CTkFont(size=13)).grid(row=6, column=2, padx=10, pady=5, sticky="ew")
        student_grade2_entry = ctk.CTkEntry(right_frame, textvariable=student_grade2_var, placeholder_text="5.55", placeholder_text_color="white")
        student_grade2_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(right_frame, text="Média:", font=ctk.CTkFont(size=13)).grid(row=8, column=1, padx=(5,2), pady=5, sticky="e")
        student_media_entry = ctk.CTkEntry(right_frame, textvariable=student_media_var, state="readonly")
        student_media_entry.grid(row=8, column=2, padx=5, pady=5)


        register_button = ctk.CTkButton(right_frame, text="Atualizar notas", command=partial(update_notas, student_id_var, student_name_var,student_grade1_var, student_grade2_var, student_media_var, success_label) , fg_color="green", hover_color="#006400")
        register_button.grid(row=10, column=2, padx=(2,5), pady=(30, 5), sticky="w")


        reset_button = ctk.CTkButton(right_frame, text="Reset", command=partial(reset_form4, student_id_var, student_name_var, student_grade1_var, student_grade2_var, student_media_var), fg_color="red", hover_color="#8B0000")
        reset_button.grid(row=10, column=3, padx=(2,5), pady=(30, 5), sticky="w")

    def open_aprrpr_window():
        cleanup_right_frame()

        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_columnconfigure(2, weight=1)
        right_frame.grid_columnconfigure(3, weight=1)

        title_label = ctk.CTkLabel(right_frame, text="Alunos Aprovados e Reprovados", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, pady=(10,30), sticky="ew", columnspan=4)
        
        # Create button frame
        button_frame = ctk.CTkFrame(right_frame, fg_color="#282828")
        button_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Create scrollable frame for the table
        table_frame = ctk.CTkScrollableFrame(right_frame, fg_color="#383838", height=400)
        table_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Configure grid weight for table frame
        right_frame.grid_rowconfigure(2, weight=1)

        # Setup table
        setup_table_frame_columns(table_frame)
        create_table_header(table_frame)

        # Create filter buttons
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        ambos_button = ctk.CTkButton(button_frame, text="Todos", command=lambda: populate_table(table_frame, "all"),  fg_color="gray", hover_color="#606060", width=120)
        ambos_button.grid(row=0, column=0, padx=10, pady=5)
        
        aprovados_button = ctk.CTkButton(button_frame, text="Aprovados", command=lambda: populate_table(table_frame, "approved"), fg_color="#0A3D0A", hover_color="#019C01", width=120)
        aprovados_button.grid(row=0, column=1, padx=10, pady=5)
        
        reprovados_button = ctk.CTkButton(button_frame, text="Reprovados", command=lambda: populate_table(table_frame, "failed"),  fg_color="salmon", hover_color="#FF5E00", width=120)
        reprovados_button.grid(row=0, column=2, padx=10, pady=5)

        populate_table(table_frame, "all")

    # Create navigation buttons
    RegButton = ctk.CTkButton(left_frame, text="Registrar Novo Usuário", command=open_register_window, fg_color="#202020")
    RegButton.pack(pady=10)

    SecondButton = ctk.CTkButton(left_frame, text="Registrar Novo Aluno", command=open_student_register_window, fg_color="#202020")
    SecondButton.pack(pady=10)

    ThirdButton = ctk.CTkButton(left_frame, text="Atualizar Informação Aluno", command=open_usi_window, fg_color="#202020")
    ThirdButton.pack(pady=10)

    FourthButton = ctk.CTkButton(left_frame, text="Atualizar notas do Aluno", command=open_usg_window, fg_color="#202020")
    FourthButton.pack(pady=10)

    FifthButton = ctk.CTkButton(left_frame, text="Situação Alunos", command=open_aprrpr_window, fg_color="#202020")
    FifthButton.pack(pady=10)

    ExitButton = ctk.CTkButton(left_frame, text="Fechar", command=lambda: on_closing(root), fg_color="#492424", hover_color="#FF0000")
    ExitButton.pack(pady=10)



