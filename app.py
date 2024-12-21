from flask import Flask, render_template, request, redirect
import sqlite3
from encryption import encrypt_message, decrypt_message

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

# Главная страница
@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM entries")
    entries = [{"id": row[0], "title": row[1], "content": decrypt_message(row[2])} for row in c.fetchall()]
    conn.close()
    return render_template("index.html", entries=entries)

# Добавление записи
@app.route("/add", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        encrypted_content = encrypt_message(content)

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO entries (title, content) VALUES (?, ?)", (title, encrypted_content))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("add_entry.html")

# Просмотр записи
@app.route("/entry/<int:entry_id>")
def view_entry(entry_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT title, content FROM entries WHERE id = ?", (entry_id,))
    row = c.fetchone()
    conn.close()

    if row:
        entry = {"title": row[0], "content": decrypt_message(row[1])}
        return render_template("view_entry.html", entry=entry)
    return "Запись не найдена!", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5007)
