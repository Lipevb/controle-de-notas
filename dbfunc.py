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
    """Close all active connection pools"""
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
        print("username already in use")
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
    """
    Fetch student data from the database based on the entered student ID.
    Returns a dictionary with student data or None if no student is found.
    """
    if not student_id:
        print("Please enter a valid Student ID.")
        return None
        
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

