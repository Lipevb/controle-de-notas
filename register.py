import hashlib
import re  # For password validation
import os  # For generating random salt
from dbfunc import update_user_db  # Import the function to update user database


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
    user.set("")
    pwd.set("")

    # Validate the password
    validation_error = validate_password(password)
    if validation_error:
        success_label.configure(text=validation_error)
        return

    # Generate a random salt
    salt = os.urandom(16).hex()

    # Hash the password with the salt
    hashed_password = hash_password(password, salt)

    update_user_db(username, salt, hashed_password)








def registertxt(user, pwd, success_label):
    username = user.get()
    password = pwd.get()
    user.set("")
    pwd.set("")

    # Validate the password
    validation_error = validate_password(password)
    if validation_error:
        success_label.configure(text=validation_error)
        return

    # Generate a random salt
    salt = os.urandom(16).hex()

    # Hash the password with the salt
    hashed_password = hash_password(password, salt)

    # Prepare the entry to store
    entry = f"{username};{salt};{hashed_password}\n"

    try:
        with open("User.txt", "r") as file:
            users = file.readlines()
    except FileNotFoundError:
        users = []

    # Check if the username already exists
    for line in users:
        stored_username, _, _ = line.strip().split(";")
        if username == stored_username:
            success_label.configure(text="Username already exists.")
            return

    # Add the new user
    users.append(entry)
    with open("User.txt", "w") as file:
        file.writelines(users)
    success_label.configure(text="User registered successfully.")

def reset_form(user_var, pass_var):
    user_var.set("")
    pass_var.set("")


def reset_form2(student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var):
        student_name_var.set("")
        student_birthday_var.set("")
        student_phone_var.set("")
        student_email_var.set("")
        student_address_var.set("")
        student_class_var .set("")



def reset_form3(student_id_var, student_name_var, student_birthday_var, student_phone_var, student_email_var, student_address_var, student_class_var):
    student_id_var.set("")
    student_name_var.set("")
    student_birthday_var.set("")
    student_phone_var.set("")
    student_email_var.set("")
    student_class_var.set("")
    student_address_var.set("")


def reset_form4(student_id_var, student_grade1, student_grade2):
    student_id_var.set("")
    student_grade2.set("")
    student_grade1.set("")
