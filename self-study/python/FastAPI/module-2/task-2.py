from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Создай модель BookUpdate для обновления книги. Сделай так, чтобы все поля (name, author, pages) 
# были опциональными (например, pages: int | None = None), чтобы пользователь мог обновить только что-то одно.

# Pydantic — это библиотека для валидации данных в Python с помощью аннотаций типов. 
# FastAPI использует её под капотом абсолютно везде.

app = FastAPI(title="API Books")

BOOKS_DB = [
    {"id": 1, "name": "Python для новичков", "author": "Иван Иванов", "pages": 300},
    {"id": 2, "name": "Современный FastAPI", "author": "Петр Петров", "pages": 450},
]

class BooksModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    author: str = Field(..., min_length=2, max_length=100)
    pages: int = Field(..., gt=0, description="Количество страниц должно быть больше 0.")

class BookUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    author: str | None = Field(default=None, min_length=2, max_length=100)
    pages: int | None = Field(default=None, gt=0)

@app.post("/api/books", status_code=201)
def create_book(book_data: BooksModel):
    """Создать новую книгу.
    Pydantic автоматически проверит, что переданы все поля,
    что pages — это число больше 0, а у строк есть нужная длина.
    """
    new_id = len(BOOKS_DB) + 1

    new_book = {
        "id": new_id,
        "name": book_data.name,
        "author": book_data.author,
        "pages": book_data.pages,
    }

    BOOKS_DB.append(new_book)

    return {"message": "Книга успешно создана!", "book": new_book}

@app.patch("/api/books/{book_id}")
def update_book(book_id: int, book_data: BookUpdate):
    """Обновление книги"""
    target_book = None
    for book in BOOKS_DB:
        if book["id"] == book_id:
            target_book = book
            break

    if not target_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book_data.name is not None:
        target_book["name"] = book_data.name
    if book_data.author is not None:
        target_book["author"] = book_data.author
    if book_data.pages is not None:
        target_book["pages"] = book_data.pages

    return {"message": "Книга успешно обновлена!", "book": target_book}