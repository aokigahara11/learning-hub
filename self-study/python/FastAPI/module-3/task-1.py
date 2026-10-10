from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

# Попробуй написать свою зависимость (например, 
# для проверки секретного заголовка в запросе x-api-key) 
# и прикрепить её через Depends к какому-нибудь эндпоинту, чтобы он защищал доступ.

app = FastAPI(title="API Books")
SECRET_KEY = "password_key"

BOOKS_DB = [
    {"id": 1, "name": "Python для новичков", "author": "Иван Иванов", "pages": 300},
    {"id": 2, "name": "Современный FastAPI", "author": "Петр Петров", "pages": 450},
]

def verify_api_key(x_api_key: str | None = Header(default=None)):
  """Проверяет заголовок 'x-api-key' в запросе."""
  if x_api_key != SECRET_KEY:
    raise HTTPException(
        status_code=401, detail="Неверный или отсутствующий API-ключ!"
    )

  return x_api_key

@app.post("/api/books/secure-add")
def secure_add_book(book_name: str, api_key: str = Depends(verify_api_key)):
    """Этот эндпоинт защищен.
    Сначала выполнится функция, и только если ключ верный,
    код дойдет до добавления книги.
    """
    return {
        "message": "Книга успешно добавлена через защищенный эндпоинт!",
        "book_name": book_name,
    }