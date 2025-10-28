import os
import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        return connection
    except KeyError as e:
        print(f"Missing required environment variable: {e}")
        return None
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None
