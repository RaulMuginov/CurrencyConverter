import sqlite3

conn = sqlite3.connect('currency_convert.db')
sql = conn.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, phone_number TEXT);')
conn.commit()

def add_user(name, phone_number, user_id):
    conn = sqlite3.connect('currency_convert.db')
    sql = conn.cursor()
    sql.execute('INSERT INTO users (user_id, name, phone_number) VALUES (?, ?, ?);', (user_id, name, phone_number))
    conn.commit()
def check_user(user_id):
    conn = sqlite3.connect('currency_convert.db')
    sql = conn.cursor()
    checker = sql.execute('SELECT * FROM users WHERE user_id=?;', (user_id, )).fetchone()
    if checker:
        return True
    elif not checker:
        return False
