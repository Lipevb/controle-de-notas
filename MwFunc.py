import hashlib
import re  
import os  
from datetime import datetime
from dbFunc import register_user_db, fetch_student_data, cad_aluno_db, update_aluno_db, fetch_notas_db, cad_notas_db
from resetforms import reset_form, reset_form2, reset_form3, reset_form4, reset_form5
import random


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>~`+=\[\]\\\/]", password):
        return "Password must contain at least one special character."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase character."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase character."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one numeric character."



def register (user, pwd, success_label):
    username = user.get()
    password = pwd.get()
    reset_form(user, pwd)

    
    validation_error = validate_password(password)
    if validation_error:
        success_label.configure(text=validation_error)
        return

    
    salt = os.urandom(16).hex()

    
    hashed_password = hash_password(password, salt)

    result = register_user_db(username, salt, hashed_password)
    if result:
        success_label.configure(text="User registered successfully.")
    else:
        success_label.configure(text="Username already exists or registration failed.")


def cad_aluno(student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel):
    student_name = student_name_var.get()
    student_birthday = student_birthday_var.get()
    student_phone = student_phone_var.get()
    student_email = student_email_var.get()
    student_address = student_address_var.get()
    student_class = student_class_var.get()

    try:
        if '/' in student_birthday:
            data = datetime.strptime(student_birthday, '%d/%m/%Y')
            data_format = data.strftime('%Y-%m-%d')
        else:
            data_format = student_birthday
    except ValueError:
        SuccessLabel.configure(text=f"Data inválida: {student_birthday}. Use o formato DD/MM/AAAA e verifique se a data é válida.")
        return
    if not all([student_name, data_format, student_phone, student_email, student_address, student_class]):
        SuccessLabel.configure(text="Please fill in all fields.")
        return

    result = cad_aluno_db(student_name, data_format, student_phone, student_email, student_address, student_class)
    if result:
        SuccessLabel.configure(text=f"Aluno {student_name} cadastrado com o id {result}.")
    else:
        SuccessLabel.configure(text="Falha ao cadastrar aluno. Por favor, tente novamente.")
    
    reset_form2(student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var)
    


def populate_entries(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel):
    student_id = student_id_var.get()
    student_data = fetch_student_data(student_id)  

    if student_data:
        student_name_var.set(student_data["nome"])
        data = student_data["data"]
        data_format = data.strftime('%d/%m/%Y')
        student_birthday_var.set(data_format)
        student_phone_var.set(student_data["telefone"])
        student_email_var.set(student_data["email"])
        student_address_var.set(student_data["end"])
        student_class_var.set(student_data["curso"])
        SuccessLabel.configure(text="Dados do aluno preenchidos com sucesso.")
    else:
        student_name_var.set("")
        student_birthday_var.set("")
        student_phone_var.set("")
        student_email_var.set("")
        student_address_var.set("")
        student_class_var.set("")
        SuccessLabel.configure(text="Nenhum aluno com esse ID encontrado.")


def update_aluno(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel):
    student_id = student_id_var.get()
    student_name = student_name_var.get()
    student_birthday = student_birthday_var.get()
    student_phone = student_phone_var.get()
    student_email = student_email_var.get()
    student_address = student_address_var.get()
    student_class = student_class_var.get()

    if '/' in student_birthday:
        data = datetime.strptime(student_birthday, '%d/%m/%Y')
        data_format = data.strftime('%Y-%m-%d')
    else:
        data_format = student_birthday

    if not all([student_id, student_name, data_format, student_phone, student_email, student_address, student_class]):
        SuccessLabel.configure(text="Please fill in all fields.")
        return

    result = update_aluno_db(student_id, student_name, student_birthday, student_phone, student_email, student_address, student_class)
    reset_form3(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var)
    if result:
        SuccessLabel.configure(text=f"Dados do aluno {student_name} atualizados com sucesso.")
    else:
        SuccessLabel.configure(text="Não foi possível atualizar os dados do aluno. Por favor, tente novamente.")


def pop_notas(student_id_var, student_name_var, student_grade1, student_grade2, student_media, SuccessLabel):
    student_id = student_id_var.get()
    student_data = fetch_student_data(student_id)  
    reset_form5(student_name_var, student_grade1, student_grade2, student_media)
    if student_data:
        
        student_name_var.set(student_data["nome"])
        
        notas = fetch_notas_db(student_id)
        if notas:
            student_grade1.set(notas["nota1"])
            student_grade2.set(notas["nota2"])
            student_media.set(notas["media"])
            SuccessLabel.configure(text="Notas encontradas.")
        else:
            student_grade1.set("")
            student_grade2.set("")
            SuccessLabel.configure(text="Notas não encontradas para esse aluno.")
        
    else:
        reset_form4(student_id_var, student_name_var, student_grade1, student_grade2, student_media)
        SuccessLabel.configure(text="Não foi possível encontrar aluno com esse ID.")


def update_notas(student_id_var, student_name_var, student_grade1, student_grade2, student_media_var, SuccessLabel):
    student_id = student_id_var.get()
    nota1_str = student_grade1.get()
    nota2_str = student_grade2.get()
    student_data = fetch_student_data(student_id)  
    nota1 = 0.0
    nota2 = 0.0
    
    if not student_data:
        reset_form4(student_id_var, student_name_var, student_grade1, student_grade2, student_media_var)
        SuccessLabel.configure(text="Nenhum aluno encontrado com esse ID.")
        return
    
    if nota1_str is not None: 
        nota1 = float(nota1_str)
        if nota1 < 0 or nota1 > 10:
            SuccessLabel.configure(text="As notas devem estar entre 0 e 10.")
            return

    if nota2_str is not None: 
        nota2 = float(nota2_str)
        if nota2 < 0 or nota2 > 10:
            SuccessLabel.configure(text="As notas devem estar entre 0 e 10.")
            return
    
    if nota1_str is not None and nota2_str is not None: media = (nota1 + nota2) / 2  
    elif nota1_str is not None and nota2_str is None: 
        media = (nota1 + nota2) / 2
    elif nota1_str is None and nota2_str is not None: 
        media = (nota1 + nota2) / 2
    else: 
        media = 0

    result = cad_notas_db(student_id, nota1, nota2, media)

    reset_form4(student_id_var, student_name_var,student_grade1, student_grade2, student_media_var)

    if result:
        SuccessLabel.configure(text=f"Notas do aluno {student_data['nome']} atualizadas com sucesso com a média: {media:.2f}")
    else:
        SuccessLabel.configure(text="Falha ao atualizar notas. Por favor, tente novamente.")


def validate_decimal_input(char,):
    if char == "":
        return True
    
    # Allow numbers, dots, and commas
    allowed_chars = "0123456789."
    
    # Check if all characters are allowed
    for c in char:
        if c not in allowed_chars:
            return False
    
    # Ensure only one decimal separator
    dot_count = char.count('.')
    comma_count = char.count(',')
    
    if dot_count + comma_count > 1:
        return False
    
    return True
