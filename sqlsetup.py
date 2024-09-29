import psycopg2
from psycopg2 import sql

# Connection parameters for the superuser (typically 'postgres')
superuser_conn_params = {
    'dbname': 'postgres', 
    'user': 'postgres', 
    'password': 'surya',  # replace with your actual superuser password
    'host': 'localhost', 
    'port': '5432'
}

# The new database, user, and password
new_db_name = 'medical_db'
new_user = 'medical_user'
new_password = 'surya'  # replace with the password you want for the new user

def create_db_and_user():
    try:
        # Establish a connection to PostgreSQL as the superuser
        print("Connecting to PostgreSQL as superuser...")
        conn = psycopg2.connect(**superuser_conn_params)
        conn.autocommit = True
        cur = conn.cursor()

        # Create a new database
        print(f"Creating database '{new_db_name}'...")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
        print(f"Database '{new_db_name}' created successfully.")

        # Create a new user and assign privileges
        print(f"Creating user '{new_user}'...")
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(new_user)), [new_password])
        print(f"User '{new_user}' created successfully.")

        # Grant superuser privileges to the new user
        print(f"Granting superuser privileges to '{new_user}'...")
        cur.execute(sql.SQL("ALTER USER {} WITH SUPERUSER").format(sql.Identifier(new_user)))
        print(f"User '{new_user}' granted superuser privileges.")

        # Close the cursor and connection
        cur.close()
        conn.close()
        print("Database setup completed successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")


create_db_and_user()