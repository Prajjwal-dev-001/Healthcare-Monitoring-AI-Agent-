import sqlite3
from datetime import datetime

conn = sqlite3.connect("health.db", check_same_thread=False)
cursor = conn.cursor()

# Medications table
cursor.execute("""
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time TEXT NOT NULL
)
""")

# Reminders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    reminder_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
)
""")

conn.commit()

def add_medicine(name, time):
    cursor.execute(
        "INSERT INTO medications (name, time) VALUES (?, ?)",
        (name, time)
    )
    conn.commit()

def get_medicines():
    cursor.execute("SELECT * FROM medications ORDER BY id DESC")
    return cursor.fetchall()

def add_reminder(medicine_name, reminder_at):
    cursor.execute(
        "INSERT INTO reminders (medicine_name, reminder_at, status) VALUES (?, ?, 'pending')",
        (medicine_name, reminder_at)
    )
    conn.commit()

def get_reminders():
    cursor.execute("SELECT * FROM reminders ORDER BY id DESC")
    return cursor.fetchall()

def mark_reminder_taken(reminder_id):
    cursor.execute(
        "UPDATE reminders SET status='taken' WHERE id=?",
        (reminder_id,)
    )
    conn.commit()

def delete_reminder(reminder_id):
    cursor.execute(
        "DELETE FROM reminders WHERE id=?",
        (reminder_id,)
    )
    conn.commit()

def get_due_reminders():
    cursor.execute("SELECT * FROM reminders WHERE status='pending'")
    rows = cursor.fetchall()

    now = datetime.now()
    due = []

    for row in rows:
        # row = (id, medicine_name, reminder_at, status)
        try:
            reminder_dt = datetime.fromisoformat(row[2])
            if reminder_dt <= now:
                due.append(row)
        except ValueError:
            pass

    return due
