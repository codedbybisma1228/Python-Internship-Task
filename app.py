from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'your_secret_key'
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            author TEXT
        )
    ''')
    conn.commit()
    conn.close()
init_db()
@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('home.html', posts=posts)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect('blog.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            flash('Registration successful. Please login.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.')
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE author = ? ORDER BY id DESC", (session['username'],))
    posts = c.fetchall()
    conn.close()
    return render_template('dashboard.html', posts=posts)
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('create_post.html')
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        c.execute("UPDATE posts SET title=?, content=? WHERE id=? AND author=?", (title, content, post_id, session['username']))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    c.execute("SELECT * FROM posts WHERE id=? AND author=?", (post_id, session['username']))
    post = c.fetchone()
    conn.close()
    return render_template('edit_post.html', post=post)
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=? AND author=?", (post_id, session['username']))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)
    db = SQLAlchemy(app)
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), unique=True, nullable=False)
        password = db.Column(db.String(150), nullable=False)
@app.route('/debug-users')
def debug_users():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users")
    users = c.fetchall()
    conn.close()
    html = "<h2>All Users (Debug)</h2><ul>"
    for user in users:
        html += f"<li>ID: {user[0]}, Username: {user[1]}, Password Hash: {user[2]}</li>"
    html += "</ul>"

    return html
