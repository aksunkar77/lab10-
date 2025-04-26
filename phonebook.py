import psycopg2

conn = psycopg2.connect(
    dbname="PhoneBook",
    user="postgres",
    password="Aksu",
    host="localhost",
    port="5432"
)
import csv

def insert_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", 
                        (row['username'], row['phone']))
    conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
def update_data():
    name = input("Enter username to update: ")
    new_phone = input("Enter new phone: ")
    cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, name))
    conn.commit()
def search_by_username():
    name = input("Search by username: ")
    cur.execute("SELECT * FROM phonebook WHERE username = %s", (name,))
    print(cur.fetchall())
def delete_user():
    choice = input("Delete by (1) username or (2) phone: ")
    if choice == "1":
        name = input("Enter username: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
    else:
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
