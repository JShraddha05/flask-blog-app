import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

conn.close()