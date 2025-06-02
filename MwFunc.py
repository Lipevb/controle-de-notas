import hashlib
import re  # For password validation
import os  # For generating random salt
from dbFunc import register_user_db, fetch_student_data, cad_aluno_db, update_aluno_db, fetch_notas_db, cad_notas_db
from resetforms import reset_form, reset_form2, reset_form3, reset_form4


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

    # Validate the password
    validation_error = validate_password(password)
    if validation_error:
        success_label.configure(text=validation_error)
        return

    # Generate a random salt
    salt = os.urandom(16).hex()

    # Hash the password with the salt
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

    if not all([student_name, student_birthday, student_phone, student_email, student_address, student_class]):
        SuccessLabel.configure(text="Please fill in all fields.")
        return

    result = cad_aluno_db(student_name, student_birthday, student_phone, student_email, student_address, student_class)
    if result:
        SuccessLabel.configure(text="Student registered successfully.")
    else:
        SuccessLabel.configure(text="Failed to register student. Please try again.")
    
    
    reset_form2(student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var)
    


def populate_entries(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel):
    student_id = student_id_var.get()
    student_data = fetch_student_data(student_id)  

    if student_data:
        student_name_var.set(student_data["name"])
        student_birthday_var.set(student_data["birthday"])
        student_phone_var.set(student_data["phone"])
        student_email_var.set(student_data["email"])
        student_address_var.set(student_data["address"])
        student_class_var.set(student_data["class"])
        SuccessLabel.configure(text="Student data populated successfully.")
    else:
        student_name_var.set("")
        student_birthday_var.set("")
        student_phone_var.set("")
        student_email_var.set("")
        student_address_var.set("")
        student_class_var.set("")
        SuccessLabel.configure(text="No student found with the given ID.")


def update_aluno(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var, SuccessLabel):
    student_id = student_id_var.get()
    student_name = student_name_var.get()
    student_birthday = student_birthday_var.get()
    student_phone = student_phone_var.get()
    student_email = student_email_var.get()
    student_address = student_address_var.get()
    student_class = student_class_var.get()

    if not all([student_id, student_name, student_birthday, student_phone, student_email, student_address, student_class]):
        SuccessLabel.configure(text="Please fill in all fields.")
        return

    result = update_aluno_db(student_id, student_name, student_birthday, student_phone, student_email, student_address, student_class)
    reset_form3(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var)
    if result:
        SuccessLabel.configure(text="Student information updated successfully.")
    else:
        SuccessLabel.configure(text="Failed to update student information. Please try again.")


def pop_notas(student_id_var, student_name_var, student_grade1, student_grade2, SuccessLabel):
    student_id = student_id_var.get()
    student_data = fetch_student_data(student_id)  

    if student_data:
        
        student_name_var.set(student_data["name"])
        
        notas = fetch_notas_db(student_id, student_data["name"])
        if notas:
            student_grade1.set(notas["grade1"])
            student_grade2.set(notas["grade2"])
            SuccessLabel.configure(text="Notas encontradas.")
        else:
            student_grade1.set("")
            student_grade2.set("")
            SuccessLabel.configure(text="Notas não encontradas para esse aluno.")
        
    else:
        reset_form4(student_id_var, student_name_var,student_grade1, student_grade2)
        SuccessLabel.configure(text="Não foi possível encontrar aluno com esse ID.")


def update_notas(student_id_var, student_name_var, student_grade1, student_grade2, SuccessLabel):
    student_id = student_id_var.get()
    student_name = student_name_var.get()
    grade1 = student_grade1.get()
    grade2 = student_grade2.get()

    if grade1 is not None and grade1 < 0 or grade1 > 10:
        SuccessLabel.configure(text="As notas devem estar entre 0 e 10.")
        return

    if grade2 is not None and grade2 < 0 or grade2 > 10:
        SuccessLabel.configure(text="As notas devem estar entre 0 e 10.")
        return
    
    if grade1 is not None and grade2 is not None: media = (grade1 + grade2) / 2  
    elif grade1 is not None and grade2 is None: media = grade1 + 0 / 2
    elif grade1 is None and grade2 is not None: media = 0 + grade2 / 2
    else: media = 0

    result = cad_notas_db(student_id, student_name, grade1, grade2, media)

    reset_form4(student_id_var, student_name_var,student_grade1, student_grade2)

    if result:
        SuccessLabel.configure(text="Notas atualizadas com sucesso.")
    else:
        SuccessLabel.configure(text="Falha ao atualizar notas. Por favor, tente novamente.")
