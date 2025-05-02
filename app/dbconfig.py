import mysql.connector
import os, time
from pathlib import Path
import dotenv

dotenv.load_dotenv(Path('.env'))

db_config_r = {
    'host': os.environ.get('host_r'),
    'user': os.environ.get('user_r'),
    'password': os.environ.get('password_r'),
    'database': 'sakila'
}


db_config_e = {
    'host': os.environ.get('host_e'),
    'user': os.environ.get('user_e'),
    'password': os.environ.get('password_e'),
    'database': 'Trotskaya_111124'
}

def connect_read():
    connR = mysql.connector.connect(**db_config_r)
    cursorR = connR.cursor()
    return connR, cursorR

def connect_write():
    connE = mysql.connector.connect(**db_config_e)
    cursorE = connE.cursor()
    return connE, cursorE

def check_connection(conn):
    """Check if the database connection is alive."""
    try:
        conn.ping(reconnect=False)
        return True
    except mysql.connector.Error:
        return False

def reconnect(config, max_retries=3):
    """Try to reconnect to the database if the connection is down."""
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**config)
            print(f"Reconnected to database on attempt {attempt + 1}")
            return conn
        except mysql.connector.Error as e:
            print(f"Reconnection attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    print("Failed to reconnect to database. Please try again later.")
    return None

def close_connections():
    mysql.connector.connect(**db_config_r).close()
    mysql.connector.connect(**db_config_e).close()