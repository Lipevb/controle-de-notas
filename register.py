import hashlib
import re  # For password validation
import os  # For generating random salt

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

def register(user, pwd, success_label):
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