from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'books.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER,
            rating REAL DEFAULT 0,
            description TEXT,
            cover_color TEXT DEFAULT '#4A90D9'
        )
    ''')
    # Seed data
    count = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    if count == 0:
        books = [
            ('Мастер и Маргарита', 'Михаил Булгаков', 'Роман', 1967, 4.9, 'Мистический роман о визите дьявола в советскую Москву.', '#E8534A'),
            ('1984', 'Джордж Оруэлл', 'Антиутопия', 1949, 4.8, 'Тоталитарное общество будущего глазами одного человека.', '#2D6A4F'),
            ('Преступление и наказание', 'Фёдор Достоевский', 'Классика', 1866, 4.7, 'Психологический роман о нравственных муках убийцы.', '#7B4F8E'),
            ('Маленький принц', 'Антуан де Сент-Экзюпери', 'Сказка', 1943, 4.9, 'Философская сказка о мальчике с другой планеты.', '#F4A261'),
            ('Дюна', 'Фрэнк Герберт', 'Фантастика', 1965, 4.7, 'Эпическая сага о пустынной планете и её обитателях.', '#E9C46A'),
            ('Гарри Поттер и философский камень', 'Дж. К. Роулинг', 'Фэнтези', 1997, 4.8, 'Начало истории юного волшебника.', '#264653'),
        ]
        conn.executemany(
            'INSERT INTO books (title, author, genre, year, rating, description, cover_color) VALUES (?,?,?,?,?,?,?)',
            books
        )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    genre_filter = request.args.get('genre', '')
    search = request.args.get('search', '')
    query = 'SELECT * FROM books'
    params = []
    conditions = []
    if genre_filter:
        conditions.append('genre = ?')
        params.append(genre_filter)
    if search:
        conditions.append('(title LIKE ? OR author LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    query += ' ORDER BY rating DESC'
    books = conn.execute(query, params).fetchall()
    genres = [r[0] for r in conn.execute('SELECT DISTINCT genre FROM books ORDER BY genre').fetchall()]
    conn.close()
    return render_template('index.html', books=books, genres=genres, current_genre=genre_filter, search=search)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        conn = get_db()
        conn.execute(
            'INSERT INTO books (title, author, genre, year, rating, description, cover_color) VALUES (?,?,?,?,?,?,?)',
            (request.form['title'], request.form['author'], request.form['genre'],
             request.form.get('year') or None, request.form.get('rating') or 0,
             request.form.get('description', ''), request.form.get('cover_color', '#4A90D9'))
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('form.html', book=None, action='add')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db()
    if request.method == 'POST':
        conn.execute(
            'UPDATE books SET title=?, author=?, genre=?, year=?, rating=?, description=?, cover_color=? WHERE id=?',
            (request.form['title'], request.form['author'], request.form['genre'],
             request.form.get('year') or None, request.form.get('rating') or 0,
             request.form.get('description', ''), request.form.get('cover_color', '#4A90D9'), id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    book = conn.execute('SELECT * FROM books WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('form.html', book=book, action='edit')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    conn = get_db()
    conn.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/books')
def api_books():
    conn = get_db()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(b) for b in books])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
