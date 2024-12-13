import sqlite3
import hashlib
import os, sys

def getpath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def create_table():
    """Creates a table for storing usernames and hashed passwords."""
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password_hash TEXT NOT NULL
                          )''')
        conn.commit()

create_table()

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Adds a new user with a hashed password to the database."""
    password_hash = hash_password(password)
    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            print("User added successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")

def check_user(username, password):
    """Checks if the provided username and password are valid."""
    password_hash = hash_password(password)
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        user = cursor.fetchone()
        if user:
            print("Login successful!")
            return user[0]
        else:
            print("Invalid username or password.")
            return -1


create_table()