import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            amount REAL,
            description TEXT,
            date TEXT,
            type TEXT,
            category TEXT
        )
    ''')
    conn.commit()

def add_transaction(conn, amount, description, category, type, date):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, description, category, type, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, description, category, type, date))
    conn.commit()

def fetch_data(conn, search_text=''):
    cursor = conn.cursor()
    if search_text:
        cursor.execute('SELECT * FROM transactions WHERE description LIKE ? ORDER BY id DESC', (f'{search_text}%',))
    else:
        cursor.execute('SELECT * FROM transactions ORDER BY id DESC')
    return cursor.fetchall()

def get_total(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
    expense = cursor.fetchone()[0] or 0
    balance = income - expense
    return income, expense, balance