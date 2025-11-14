#!/usr/bin/env python3
"""
Simple Vulnerable Test Application for APT Pipeline Validation
Contains known vulnerabilities for testing purposes
"""

from flask import Flask, request, render_template_string, redirect
import sqlite3
import os

app = Flask(__name__)

# Create a simple database with test data
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123', 'admin@test.com')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'userpass', 'user@test.com')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template_string("""
    <html>
    <head><title>Test Vulnerable App</title></head>
    <body>
        <h1>Welcome to Test App</h1>
        <a href="/login">Login</a> | <a href="/search">Search</a> | <a href="/user/1">User Profile</a>
    </body>
    </html>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # VULNERABLE: SQL Injection
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return f"Welcome {user[1]}!"
        else:
            return "Login failed"

    return render_template_string("""
    <html>
    <body>
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """)

@app.route('/search')
def search():
    query = request.args.get('q', '')

    # VULNERABLE: XSS
    return render_template_string(f"""
    <html>
    <body>
        <h2>Search Results for: {query}</h2>
        <form>
            <input name="q" value="{query}">
            <input type="submit" value="Search">
        </form>
    </body>
    </html>
    """)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    # VULNERABLE: IDOR - no access control
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        return render_template_string(f"""
        <html>
        <body>
            <h2>User Profile</h2>
            <p>ID: {user[0]}</p>
            <p>Username: {user[1]}</p>
            <p>Email: {user[2]}</p>
        </body>
        </html>
        """)
    else:
        return "User not found"

@app.route('/redirect')
def redirect_test():
    url = request.args.get('url', '/')
    # VULNERABLE: Open Redirect
    return redirect(url)

@app.route('/file')
def file_access():
    filename = request.args.get('file', 'test.txt')
    # VULNERABLE: Directory Traversal (simplified)
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return f"File content: {content}"
    except:
        return "File not found"

if __name__ == '__main__':
    print("🚨 Starting VULNERABLE test application on http://localhost:5000")
    print("⚠️  This app contains intentional vulnerabilities for testing!")
    print("Known vulnerabilities:")
    print("  - SQL Injection: /login (username/password)")
    print("  - XSS: /search?q=<script>alert(1)</script>")
    print("  - IDOR: /user/1 vs /user/2")
    print("  - Open Redirect: /redirect?url=http://evil.com")
    print("  - Directory Traversal: /file?file=../../../etc/passwd")
    print("Press Ctrl+C to stop...")

    # Remove threaded=True for Windows compatibility
    app.run(host='127.0.0.1', port=5000, debug=False)