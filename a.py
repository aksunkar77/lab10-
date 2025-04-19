# in this file i will practice with PostgreSQL + Python - PhoneBook & Snake Game Integration

import psycopg2
import csv


def connect():
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )

def create_phonebook_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()

def update_phonebook(name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()

def search_phonebook(keyword):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def delete_from_phonebook(keyword):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (keyword, keyword))
    conn.commit()
    cur.close()
    conn.close()


def create_snake_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) REFERENCES users(username),
            score INT,
            level INT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username = %s", (username,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        level = 1
    else:
        cur.execute("SELECT MAX(level) FROM user_score WHERE username = %s", (username,))
        result = cur.fetchone()[0]
        level = result if result else 1
    conn.commit()
    cur.close()
    conn.close()
    return level

def save_score(username, score, level):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_score (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
    conn.commit()
    cur.close()
    conn.close()

