import os
from psycopg2 import pool, IntegrityError
from dotenv import load_dotenv

# Global connection pool (create once, reuse many times)
_connection_pool = None
active_pools = []

def get_connection_pool():
    """Get or create a single global connection pool"""
    global _connection_pool
    if _connection_pool is None:
        load_dotenv()
        connection_string = os.getenv('DATABASE_URL')
        
        _connection_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections in the pool
            10,  # Maximum number of connections in the pool
            connection_string
        )
        
        # Track this pool
        active_pools.append(_connection_pool)
    
    return _connection_pool

def cleanup_connections():

    global active_pools, _connection_pool
    for pool_obj in active_pools:
        try:
            if pool_obj:
                pool_obj.closeall()
                print("Connection pool closed")
        except Exception as e:
            print(f"Error closing connection pool: {e}")
    active_pools.clear()
    _connection_pool = None

def fetch_password_db(username):
    connection_pool = get_connection_pool()
    conn = None
    cur = None
    
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        cur = conn.cursor()

        # Execute SQL commands
        cur.execute("SELECT addon, password FROM users WHERE username=%s;", (username,))
        log = cur.fetchone()

        if log:
            return {
                "addon": log[0],
                "password": log[1]
            }
        else:
            print("No user found with the given username.")
            return None
            
    except Exception as e:
        print(f"Database error: {e}")
        return None
        
    finally:
        # Only close cursor and return connection to pool
        # DON'T close the entire pool
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

def register_user_db(username, salt, hashed_password):
    connection_pool = get_connection_pool()
    conn = None
    cur = None
    
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, addon, password) VALUES(%s, %s, %s) RETURNING id;", 
                   (username, salt, hashed_password))
        user_id = cur.fetchone()[0]

        conn.commit()
        
        print(f"User {username} added with ID {user_id}")
        return True
        
    except IntegrityError:
        print("Username already in use")
        if conn:
            conn.rollback()
        return False
        
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)



def cad_aluno_db(student_name, student_birthday, student_phone, student_email, student_address, student_class):
    connection_pool = get_connection_pool()
    conn = None
    cur = None
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("INSERT INTO students (nome, data_nascimento, telefone, email, endereço, curso) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;", (student_name, student_birthday, student_phone, student_email, student_address, student_class))
        aluno_id = cur.fetchone()[0]
        conn.commit()

        print(f"Student {student_name} added successfully with id {aluno_id}.")
        return True
    except IntegrityError:
        print("Failed to register student. Please try again.")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)


def fetch_student_data(student_id):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        cur = conn.cursor()
        
        cur.execute("SELECT nome, data_nascimento, telefone, email, endereço, curso FROM students WHERE id = %s", (student_id,))
        result = cur.fetchone()

        if result:
            return {
                "nome": result[0],
                "data": result[1],
                "telefone": result[2],
                "email": result[3],
                "end": result[4],
                "curso": result[5],
            }
        else:
            print("No student found with the given ID.")
            return None
            
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)


def update_aluno_db(student_id, student_name, student_birthday, student_phone, student_email, student_address, student_class):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("""UPDATE students SET nome = %s, data_nascimento = %s, telefone = %s, email = %s, endereço = %s, curso = %s WHERE id = %s""", (student_name, student_birthday, student_phone, student_email, student_address, student_class, student_id))
        
        if cur.rowcount == 0:
            print("No student found with the given ID.")
            return False
        
        conn.commit()
        print(f"Student {student_name} with id {student_id} updated successfully.")
        return True
    except IntegrityError:
        print("Failed to update student. Please try again.")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
        

def fetch_notas_db(student_id, student_name):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("SELECT nota1, nota2 FROM notas WHERE aluno_id = %s AND aluno_nome = %s", (student_id, student_name))
        result = cur.fetchone()

        if result:
            return {
                "grade1": result[0],
                "grade2": result[1],
            }
        else:
            print("No grades found for the given student.")
            return None

    except IntegrityError:
        print("Failed to fetch grades. Please try again.")
        if conn:
            conn.rollback()
        return None
            
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)


def cad_notas_db(student_id, student_name, grade1, grade2, media):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        if grade1 is not None and grade2 is not None:
            cur.execute("INSERT INTO notas (aluno_id, aluno_nome, nota1, nota2) VALUES (%s, %s, %f, %f, %f)", (student_id, student_name, grade1, grade2, media))
            conn.commit()
        else:
            print("Grades cannot be None.")
            return False
        
        if cur.rowcount == 0:
            print("Failed to add grades. Please check the student ID and name.")
            return False
                
        print(f"Grades for student {student_name} with ID {student_id} added successfully.")
        return True

    except IntegrityError:
        print("Failed to register grades. Please try again.")
        if conn:
            conn.rollback()
        return False
        
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

