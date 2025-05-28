import sqlite3
   





def fetch_student_data(student_id):
    """
    Fetch student data from the database based on the entered student ID.
    Returns a dictionary with student data or None if no student is found.
    """
    if not student_id:
        print("Please enter a valid Student ID.")
        return None

    try:
        # Connect to the database
        conn = sqlite3.connect("students.db")  # Replace with your database file
        cursor = conn.cursor()

        # Query the database for the student data
        cursor.execute("SELECT name, birthday, phone, email, address, class FROM students WHERE id = ?", (student_id,))
        result = cursor.fetchone()

        conn.close()

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
