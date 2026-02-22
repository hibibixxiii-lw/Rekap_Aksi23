import sqlite3

DB_NAME = "database_aksi.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            debit INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_data(nama, debit):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO aksi (nama, debit)
        VALUES (?, ?)
    """, (nama, debit))
    conn.commit()
    conn.close()

def get_all_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aksi")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_last():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM aksi
        WHERE id = (SELECT MAX(id) FROM aksi)
    """)
    conn.commit()
    conn.close()

def delete_all():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aksi")
    conn.commit()
    conn.close()

def get_total_debit():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(debit) FROM aksi")
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0
