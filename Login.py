import hashlib
from dbFunc import fetch_password_db



def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def login(user, pwd, success_label):

    usr = user
    pwd = pwd

    user_data = fetch_password_db(usr)
   
    if  user_data:
        password = user_data['password']
        salt = user_data['addon']
        hashed_password = hash_password(pwd, salt)
        if hashed_password != password:
            success_label.configure(text="Usuário ou senha incorretos.")
            return False
        success_label.configure(text="Login bem-sucedido!")
        return True
    elif usr == "Admin" and pwd == "Admin":
        success_label.configure(text="Admin login bem-sucedido!")
        return True
    else:
        success_label.configure(text="Usuário ou senha incorretos.")
        return False

