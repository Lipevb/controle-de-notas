import os
from psycopg2 import pool, IntegrityError
from dotenv import load_dotenv   


def update_user_db(username, salt, hashed_password):

    username_new = username
    salt_new = salt
    hashed_password_new = hashed_password

    # Load .env file
    load_dotenv()

    # Get the connection string from the environment variable
    connection_string = os.getenv('DATABASE_URL')

    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections in the pool
        10,  # Maximum number of connections in the pool
        connection_string
    )

    # Check if the pool was created successfully
    if connection_pool:
        print("Connection pool created successfully")

    # Get a connection from the pool
    conn = connection_pool.getconn()

    # Create a cursor object
    cur = conn.cursor()

    # Execute SQL commands to retrieve the current time and version from PostgreSQL
    cur.execute('SELECT username FROM users;')
    usernames = cur.fetchall()

    # Check if username already exists
    for user in usernames:
        if user[0] == username_new:
            print("username already in use")
            cur.close()
            connection_pool.putconn(conn)
            connection_pool.closeall()
            return

    try:
        cur.execute('INSERT INTO users (username, addon, password) VALUES(%s, %s, %s) RETURNING id;', (username_new, salt_new, hashed_password_new))
        user_id = cur.fetchone()[0]
        print(f"User {username_new} added with ID {user_id}")
    except IntegrityError:
        print("username already in use")

    # Close the cursor and return the connection to the pool
    cur.close()
    connection_pool.putconn(conn)

    # Close all connections in the pool
    connection_pool.closeall()

    


def fetch_student_data(student_id):
    """
    Fetch student data from the database based on the entered student ID.
    Returns a dictionary with student data or None if no student is found.
    """
    if not student_id:
        print("Please enter a valid Student ID.")
        return None

    try:
        # Load .env file
        load_dotenv()

    # Get the connection string from the environment variable
        connection_string = os.getenv('DATABASE_URL')

    # Create a connection pool
        connection_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections in the pool
            10,  # Maximum number of connections in the pool
            connection_string
        )

    # Check if the pool was created successfully
        if connection_pool:
            print("Connection pool created successfully")

    # Get a connection from the pool
        conn = connection_pool.getconn()

    # Create a cursor object
        cur = conn.cursor()
        cur.execute("SELECT name, birthday, phone, email, address, class FROM students WHERE id = %s", (student_id,))
        result = cur.fetchone()

        cur.close()
        connection_pool.putconn(conn)

        connection_pool.closeall()
        # Check if a result was found

        if result:
            # Return the fetched data as a dictionary
            return {
                "name": result[0],
                "birthday": result[1],
                "phone": result[2],
                "email": result[3],
                "address": result[4],
                "class": result[5],
            }
        else:
            print("No student found with the given ID.")
            return None
    except Exception as e:
        print(f"Error fetching student data: {e}")
        return None
