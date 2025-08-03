import sqlite3
from datetime import datetime

DB_NAME = "smart_ticketing.db"

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            wallet REAL DEFAULT 0,
            photo_path TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT,
            entry_time TEXT,
            exit_time TEXT,
            distance_km REAL,
            fare REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT,
            amount REAL,
            type TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def passenger_exists(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM passengers WHERE name = ?", (name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_passenger(name, wallet=0.0, photo_path=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO passengers (name, wallet, photo_path) VALUES (?, ?, ?)",
        (name, wallet, photo_path)
    )
    conn.commit()
    conn.close()

def get_passenger(name):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passengers WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_wallet(name, amount, transaction_type=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE passengers SET wallet = ? WHERE name = ?", (amount, name))
    conn.commit()
    if transaction_type:
        cursor.execute(
            "INSERT INTO transactions (passenger_name, amount, type, timestamp) VALUES (?, ?, ?, ?)",
            (name, amount, transaction_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
    conn.close()

def log_trip(name, entry_time, exit_time=None, distance_km=None, fare=None):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trips (passenger_name, entry_time, exit_time, distance_km, fare) VALUES (?, ?, ?, ?, ?)",
        (name, entry_time, exit_time, distance_km, fare)
    )
    conn.commit()
    conn.close()

def update_trip_exit(name, exit_time, distance_km, fare):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE trips
        SET exit_time = ?, distance_km = ?, fare = ?
        WHERE passenger_name = ? AND exit_time IS NULL
    """, (exit_time, distance_km, fare, name))
    conn.commit()
    conn.close()

def get_all_trips():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips ORDER BY entry_time DESC")
    trips = cursor.fetchall()
    conn.close()
    return trips
