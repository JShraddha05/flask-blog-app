from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

import os
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    ''')
    
    conn.close()

# Call this when app starts
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)



@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                     (title, content, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)