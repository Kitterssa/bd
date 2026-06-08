Cтарт
```
pip install -r requirements.txt
python app.py
```
База данных SQLite
| Поле | Тип | Описание |
|---|---|---|
| id | INTEGER | Первичный ключ |
| title | TEXT | Название книги |
| author | TEXT | Автор |
| genre | TEXT | Жанр |
| year | INTEGER | Год издания |
| rating | REAL | Рейтинг 0–5 |
| description | TEXT | Описание |
| cover_color | TEXT | Цвет обложки (HEX) |

Ручное изменение базы через SQLite

```bash
Открыть базу
sqlite3 books.db
Примеры команд
.tables
SELECT * FROM books;
UPDATE books SET rating=5 WHERE id=1;
DELETE FROM books WHERE id=3;
INSERT INTO books (title, author, genre) VALUES ('Название', 'Автор', 'Жанр');
.quit
```
API
```
GET /api/books      → JSON массив всех книг
```
