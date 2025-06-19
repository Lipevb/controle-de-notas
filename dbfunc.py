import os
from psycopg2 import pool, IntegrityError
from dotenv import load_dotenv


_connection_pool = None
active_pools = []

def get_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        load_dotenv()
        connection_string = os.getenv('DATABASE_URL')
        
        _connection_pool = pool.SimpleConnectionPool(
            1,
            10,
            connection_string
        )

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
        conn = connection_pool.getconn()
        cur = conn.cursor()

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
        return aluno_id
    except IntegrityError:
        print("Failed to register student. Please try again.")
        if conn:
            conn.rollback()
        return None
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return None
    
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
        

def fetch_notas_db(student_id):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("SELECT nota1, nota2, media FROM notas WHERE aluno_id = %s", (student_id,))
        result = cur.fetchone()

        if result:
            return {
                "nota1": result[0],  
                "nota2": result[1],  
                "media": result[2]
            }
        else:
            print("No grades found for the given student.")
            return None

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)


def cad_notas_db(student_id, grade1, grade2, media):
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        if grade1 is None or grade2 is None or media is None:
            print("Grades and media cannot be None.")
            return False

        cur.execute("SELECT aluno_id FROM notas WHERE aluno_id = %s", (student_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""UPDATE notas SET nota1 = %s, nota2 = %s, media = %s WHERE aluno_id = %s""", (grade1, grade2, media, student_id))

            if cur.rowcount > 0:
                conn.commit()
                print(f"Grades for student ID {student_id} updated successfully.")
                return True
            else:
                print(f"No grades found to update for student ID {student_id}.")
                return False
            
        else:
            cur.execute("""INSERT INTO notas (aluno_id, nota1, nota2, media) VALUES (%s, %s, %s, %s)""", (student_id, grade1, grade2, media))
            conn.commit()
            print(f"Grades for student ID {student_id} added successfully.")
            return True

    except IntegrityError as e:
        print(f"Database integrity error: {e}")
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

def fetch_all_students_with_grades():
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.id, s.nome, n.nota1, n.nota2, n.media
            FROM students s
            LEFT JOIN notas n ON s.id = n.aluno_id
            ORDER BY s.id
        """)
        results = cur.fetchall()

        students_data = []
        for result in results:
            students_data.append({
                "id": result[0],
                "nome": result[1],
                "nota1": result[2] if result[2] is not None else "N/A",
                "nota2": result[3] if result[3] is not None else "N/A",
                "media": result[4] if result[4] is not None else "N/A"
            })
        
        return students_data

    except Exception as e:
        print(f"Error fetching all students: {e}")
        return []
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

def fetch_approved_students():
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.id, s.nome, n.nota1, n.nota2, n.media
            FROM students s
            INNER JOIN notas n ON s.id = n.aluno_id
            WHERE n.media >= 7.0
            ORDER BY s.id
        """)
        results = cur.fetchall()

        students_data = []
        for result in results:
            students_data.append({
                "id": result[0],
                "nome": result[1],
                "nota1": result[2],
                "nota2": result[3],
                "media": result[4]
            })
        
        return students_data

    except Exception as e:
        print(f"Error fetching approved students: {e}")
        return []
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)

def fetch_failed_students():
    connection_pool = get_connection_pool()
    conn = None
    cur = None

    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.id, s.nome, n.nota1, n.nota2, n.media
            FROM students s
            INNER JOIN notas n ON s.id = n.aluno_id
            WHERE n.media < 7.0
            ORDER BY s.id
        """)
        results = cur.fetchall()

        students_data = []
        for result in results:
            students_data.append({
                "id": result[0],
                "nome": result[1],
                "nota1": result[2],
                "nota2": result[3],
                "media": result[4]
            })
        
        return students_data

    except Exception as e:
        print(f"Error fetching failed students: {e}")
        return []
        
    finally:
        if cur:
            cur.close()
        if conn:
            connection_pool.putconn(conn)