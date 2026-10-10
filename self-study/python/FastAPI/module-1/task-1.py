from fastapi import FastAPI, HTTPException

# Практическое задание: Создать базовое приложение каталога книг. 
# эндпоинты для получения списка книг с фильтрацией через query-параметры, 
# получения книги по ID и выброса ошибки 404 Not Found, если книга не найдена.

app = FastAPI(title="API Books")

@app.get("/api/status")
def api_status():
    """Получить текущий статус API"""
    print("[INFO] API работает!")
    return {"code": 200, "message": "API работает!", "status": "ok"}


@app.get("/api/books/{book_id}")
def get_book_by_id(book_id: int):
    """Получить книгу по ID (простая имитация)"""
    # Допустим, у нас есть только книга с id = 1
    if book_id != 1:
        raise HTTPException(status_code=404, detail="Не удалось найти книгу!")

    return {
        "book": {
            "id": book_id,
            "name": "Python для новичков",
            "author": "Иван Иванов",
        }
    }


@app.get("/api/books")
def get_books_list(author: str | None = None):
    """Получить список книг с необязательным query-параметром author"""
    # Псевдо-данные для примера
    books = [
        {"id": 1, "name": "Python для новичков", "author": "Иван Иванов"},
        {"id": 2, "name": "Современный FastAPI", "author": "Петр Петров"},
    ]

    # Если передали фильтр по автору в query-параметрах (?author=...)
    if author:
        result = []
        for book in books:
            if author.lower() in book["author"].lower():
                result.append(book)
                return {"books": result}

    return {"books": books}
    