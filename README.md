# 📚 Книжная полка

Простой каталог книг на Flask + SQLite.

## Структура проекта

```
bookstore/
├── app.py              # Flask-приложение (маршруты, логика)
├── books.db            # SQLite база данных (создаётся автоматически)
├── requirements.txt    # Зависимости Python
├── templates/
│   ├── index.html      # Главная страница (каталог)
│   └── form.html       # Форма добавления / редактирования
└── README.md
```

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Запустить сервер
python app.py

# 3. Открыть в браузере
http://localhost:5000
```

## Возможности

| Функция | Описание |
|---|---|
| 📖 Каталог | Просмотр всех книг с обложками |
| 🔍 Поиск | Поиск по названию и автору |
| 🏷️ Фильтр | Фильтрация по жанру |
| ➕ Добавление | Форма добавления новой книги |
| ✏️ Редактирование | Изменение любых полей книги |
| 🗑️ Удаление | Удаление книги с подтверждением |
| 🔌 API | `GET /api/books` — JSON-список всех книг |

## База данных (SQLite)

Таблица `books`:

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

### Ручное изменение базы через SQLite

```bash
# Открыть базу напрямую
sqlite3 books.db

# Примеры команд SQL:
.tables                          -- список таблиц
SELECT * FROM books;             -- все книги
UPDATE books SET rating=5 WHERE id=1;
DELETE FROM books WHERE id=3;
INSERT INTO books (title, author, genre) VALUES ('Название', 'Автор', 'Жанр');
.quit
```

## API

```
GET /api/books      → JSON массив всех книг
```
