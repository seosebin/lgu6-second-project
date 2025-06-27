import sqlite3

def create_user_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_user_details():
    conn = sqlite3.connect('details.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(100),
            symptoms VARCHAR(150),
            disease TEXT NOT NULL,
            item1 TEXT NOT NULL,
            item2 TEXT NOT NULL,
            item3 TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

