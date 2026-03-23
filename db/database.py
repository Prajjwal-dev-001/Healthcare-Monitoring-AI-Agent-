import sqlite3

conn = sqlite3.connect("health.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    time TEXT
)
""")

conn.commit()

def add_medicine(name, time):
    cursor.execute("INSERT INTO medications (name, time) VALUES (?, ?)", (name, time))
    conn.commit()

def get_medicines():
    cursor.execute("SELECT * FROM medications")
    return cursor.fetchall()