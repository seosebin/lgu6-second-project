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

import sqlite3

def add_user_details():
    conn = sqlite3.connect('details.db')
def create_user_symptoms_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(100),
            fever INTEGER CHECK(fever IN (0, 1)),
            cough INTEGER CHECK(cough IN (0, 1)),
            fatigue INTEGER CHECK(fatigue IN (0, 1)),
            difficulty_breathing INTEGER CHECK(difficulty_breathing IN (0, 1)),
            blood_pressure TEXT CHECK(blood_pressure IN ('low', 'normal', 'high')),
            cholesterol TEXT CHECK(cholesterol IN ('low', 'normal', 'high'))
        )
    ''')
    conn.commit()
    conn.close()

def create_user_details_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(100),
            symptoms VARCHAR(150),
            disease TEXT NOT NULL,
            item1 TEXT NOT NULL,
            item2 TEXT NOT NULL,
            item3 TEXT NOT NULL,
            age INTEGER,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_user(username, password, gender, age):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, gender, age) VALUES (?, ?, ?, ?)",
                   (username, password, gender, age))
    conn.commit()
    conn.close()

def insert_user_symptoms(user_id, fever, cough, fatigue, difficulty_breathing, blood_pressure, cholesterol):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_symptoms 
        (user_id, fever, cough, fatigue, difficulty_breathing, blood_pressure, cholesterol)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, fever, cough, fatigue, difficulty_breathing, blood_pressure, cholesterol))
    conn.commit()
    conn.close()

def insert_user_details(user_id, symptoms, disease, item1, item2, item3):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO details (user_id, symptoms, disease, item1, item2, item3)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, symptoms, disease, item1, item2, item3))
    conn.commit()
    conn.close()
