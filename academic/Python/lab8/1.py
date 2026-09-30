# Пусть дана некоторая директория (папка). Посчитайте количество файлов в данной директории (папке) и выведите на экран.

from pathlib import Path

path = Path("academic/Python/8")
file_count = 0

for item in path.iterdir():
    if item.is_file():
        file_count += 1

print(f"Количество файлов: {file_count}")
