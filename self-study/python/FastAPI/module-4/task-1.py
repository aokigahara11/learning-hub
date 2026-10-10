from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DB = [
    {
        "username": "aokigahara",
        "password": pwd_context.hash("password123"),
    },
    {
        "username": "zxcursed",
        "password": pwd_context.hash("shadowfiend993"),
    },
]

BOOKS_DB = [
    {"id": 1, "name": "Python для новичков", "author": "Иван Иванов", "pages": 300},
    {"id": 2, "name": "Современный FastAPI", "author": "Петр Петров", "pages": 450},
]

# Создай эндпоинт /register, который принимает модель UserCreate (username, password) 
# и сохраняет пользователя в «базу» (пока можно в обычный список словарей, 
# предварительно захешировав пароль с помощью passlib.context.CryptContext).

# Доработай эндпоинт /token так, чтобы он проверял пользователя не по 
# жестко зашитым "admin"/"secret", а искал его в твоем словаре/списке пользователей и сверял хеш пароля.

# Защити эндпоинты создания и удаления книг из предыдущих модулей так, 
# чтобы их мог выполнять только авторизованный пользователь.

app = FastAPI(title="API Books")
SECRET_KEY = "password_key"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="API Books")
SECRET_KEY = "password_key"
ALGORITHM = "HS256"

# Настройка схемы для OAuth2 / JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)


class BooksModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    author: str = Field(..., min_length=2, max_length=100)
    pages: int = Field(..., gt=0, description="Количество страниц больше 0.")


# Зависимость для проверки JWT-токена и получения текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Невалидный токен или истек срок"
        )

@app.post("/register")
def register_user(user_data: UserCreate):
    """Регистрирует нового пользователя"""
    for user in USERS_DB:
        if user["username"] == user_data.username:
            raise HTTPException(
                status_code=400, detail="Юзер уже существует"
            )

    hashed_password = pwd_context.hash(user_data.password)

    new_user = {"username": user_data.username, "password": hashed_password}

    USERS_DB.append(new_user)

    return {
        "message": "Пользователь успешно зарегистрирован!",
        "username": user_data.username,
    }


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    found_user = None
    for user in USERS_DB:
        if user["username"] == form_data.username:
            found_user = user
            break

    # Проверяем существование пользователя и правильность хэша пароля
    if not found_user or not pwd_context.verify(form_data.password, found_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерируем JWT-токен
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": found_user["username"], "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer"}


@app.post("/api/books", status_code=201)
def create_book(book_data: BooksModel, current_user: str = Depends(get_current_user)):
    """Создать новую книгу (доступно только авторизованному пользователю)."""
    new_id = len(BOOKS_DB) + 1

    new_book = {
        "id": new_id,
        "name": book_data.name,
        "author": book_data.author,
        "pages": book_data.pages,
    }

    BOOKS_DB.append(new_book)

    return {
        "message": f"Книга успешно создана пользователем {current_user}!",
        "book": new_book,
    }

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, current_user: str = Depends(get_current_user)):
    """Удалить книгу по ID (доступно только авторизованному пользователю)."""
    book_to_delete = None
    for book in BOOKS_DB:
        if book["id"] == book_id:
            book_to_delete = book
            break

    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    BOOKS_DB.remove(book_to_delete)

    return {
        "message": f"Книга успешно удалена пользователем {current_user}",
        "deleted_book": book_to_delete,
    }
