import sqlite3
from pathlib import Path
from typing import Optional

DB_DIR = Path("academic/Python/10/2/data")
USERS_DB_PATH = DB_DIR / "database.db"

conn: Optional[sqlite3.Connection] = None


class Core:
    @staticmethod
    def init_db():
        """Создает папку и инициализирует основное соединение"""
        global conn
        DB_DIR.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(USERS_DB_PATH, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")

    @staticmethod
    def close_all_connections():
        """Закрывает все соединения"""
        if conn:
            conn.close()


class Employees:
    """
    1) Добавьте сотрудников
        Добавьте трех сотрудников в таблицу с уникальными зарплатами.
    2) Посмотреть список сотрудников
        Выведите полный список сотрудников, включая их зарплаты.
    3) Повышение зарплаты
        Повысьте зарплату одному сотруднику на 10%.
    4) Найти сотрудника по фамилии
        Найдите сотрудника по заданной вами фамилии.
    5) Удалить сотрудника
        Удалите сотрудника с минимальной зарплатой.
    """

    @staticmethod
    def create_table():
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                salary INTEGER 
            )     
        """
        )
        conn.commit()

    @staticmethod
    def add(first_name: str, last_name: str, salary: int):
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (first_name, last_name, salary) VALUES (?, ?, ?)",
            (first_name, last_name, salary),
        )
        conn.commit()

    @staticmethod
    def print_data():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")

        for row in cursor.fetchall():
            print(row)

    @staticmethod
    def increase():
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET salary = ROUND(salary * 1.1)")
            conn.commit()
        except Exception as e:
            print(f"Ошибка при увеличении заработной платы: {e}")

    @staticmethod
    def find(last_name: str):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM employees WHERE last_name = ?", (last_name,)
        )

        results = cursor.fetchall()

        if results:
            print(f"Успешно найдено сотрудников: {len(results)}")
            for employe in results:
                print(employe)
        else:
            print(f"Сотрудник с фамилией '{last_name}' не найден.")

    @staticmethod
    def delete():
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM employees WHERE salary = (SELECT MIN(salary) FROM employees);"
            )
            conn.commit()
        except Exception as e:
            print(
                f"Ошибка при удалении сотрудника с минимальной заработной платой: {e}"
            )


class Books:
    """
    1) Добавление книг
        Добавьте хотя бы пять книг в таблицу (используйте реальные названия и авторов).
    2) Отображение всех книг
        Напечатайте список всех книг с подробной информацией (заголовком, автором и годом публикации).
    3)  Поиск по названию
        Найдите книгу по заданному вами фрагменту заголовка.
    4)  Корректировка данных
        Исправьте год издания одной из книг.
    5)  Количество книг по годам
        Узнайте, сколько книг было издано в разные годы.
    """

    @staticmethod
    def create_table():
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                year_published INTEGER 
            )     
        """
        )
        conn.commit()

    @staticmethod
    def add(title: str, author: str, year_published: int):
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year_published) VALUES (?, ?, ?)",
            (title, author, year_published),
        )
        conn.commit()

    @staticmethod
    def print_data():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")

        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(
                    f"ID: {row[0]} | Название: '{row[1]}' | Автор: {row[2]} | Год: {row[3]}"
                )
        else:
            print("Список книг пуст.")

    @staticmethod
    def find(title: str):
        cursor = conn.cursor()
        pattern = f"%{title}%"
        cursor.execute(
            "SELECT * FROM books WHERE title LIKE ?", (pattern,)
        )

        results = cursor.fetchall()

        if results:
            print(f"Успешно найдено книг: {len(results)}")
            for book in results:
                print(book)
        else:
            print(f"Книга с названием '{title}' не найдена.")

    @staticmethod
    def edit_year(target_title, new_year):
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE books SET year_published = ? WHERE title = ?",
            (new_year, target_title),
        )

        conn.commit()

        if cursor.rowcount > 0:
            print(
                f"Год для книги '{target_title}' успешно изменен на {new_year}."
            )
        else:
            print(f"Книга с названием '{target_title}' не найдена.")

    @staticmethod
    def count_books_by_year(target_year):
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM books WHERE year_published = ?",
            (target_year,),
        )

        count = cursor.fetchone()[0]
        print(f"Количество книг за {target_year} год: {count}")
        return count


def init():
    Books.create_table()
    Employees.create_table()


def MainMenu(mode: int):
    if mode == 1:
        Employees.add("Алексей", "Воронов", 170000)
        Employees.add("Екатерина", "Смирнова", 90000)
        Employees.add("Дмитрий", "Соколов", 120000)

        while True:
            print(
                """
                Работа с таблицей работников.
                ===== Главное меню =====
                1. Добавить сотрудника
                2. Просмотр всех сотрудников
                3. Повышение зарплаты
                4. Найти сотрудника по фамилии
                5. Удалить сотрудника с минимальной ЗП
            """
            )

            choice = int(input("Введите номер действия: "))

            match choice:
                case 1:
                    first_name, last_name = input(
                        "Введите имя и фамилию через пробел: "
                    ).split()
                    salary = int(input("Введите заработную плату: "))
                    Employees.add(first_name, last_name, salary)
                case 2:
                    Employees.print_data()
                case 3:
                    Employees.increase()
                case 4:
                    last_name = input("Введите фамилию: ")
                    Employees.find(last_name)
                case 5:
                    Employees.delete()
                case _:
                    print("Некорректный ввод! Попробуйте снова")
    else:
        Books.add("Преступление и наказание", "Фёдор Достоевский", 1866)
        Books.add("Мастер и Маргарита", "Михаил Булгаков", 1967)
        Books.add("Сто лет одиночества", "Габриэль Гарсиа Маркес", 1967)
        Books.add("1984", "Джордж Оруэлл", 1949)
        Books.add("Граф Монте-Кристо", "Александр Дюма", 1844)
        
        while True:
            print(
                """
                Работа с таблицей книг.
                ===== Главное меню =====
                1. Добавить книгу
                2. Показать все книги
                3. Поиск по названию
                4. Изменить год книги
                5. Получить количество с конкретным годом
            """
            )

            choice = int(input("Введите номер действия: "))

            match choice:
                case 1:
                    title = input("Введите название книги: ")
                    author = input("Введите автора: ")
                    year_published = int(input("Введите год издания: "))
                    Books.add(title, author, year_published)
                case 2:
                    Books.print_data()
                case 3:
                    title = input("Введите название книги: ")
                    Books.find(title)
                case 4:
                    title = input("Введите название книги: ")
                    year = int(input("Введите новый год издания: "))
                    Books.edit_year(title, year)
                case 5:
                    year = int(input("Введите год: "))
                    Books.count_books_by_year(year)
                case _:
                    print("Некорректный ввод! Попробуйте снова")


if __name__ == "__main__":
    Core.init_db()
    init()
    MainMenu(mode=1)