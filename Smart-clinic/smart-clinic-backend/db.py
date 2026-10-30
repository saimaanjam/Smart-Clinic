import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="anjam_project_smart_clinic"
    )

# Test connection
if __name__ == "__main__":
    conn = get_db_connection()
    print("Database connection successful!")
    conn.close()
