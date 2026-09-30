# Пусть дана матрица чисел размером NхN. 
# Представьте данную матрицу в виде списка. Выведите результат сложения всех элементов матрицы.

from random import randint

n = int(input("Введите размер матрицы N: "))
matrix = []

# Внешний цикл создает N строк
for i in range(n):
    row = []
    for j in range(n):
        row.append(randint(1, 10))  # Случайное число от 1 до 10
        
    matrix.append(row)  # Добавляем готовую строку в матрицу

flat_list = []

for row in matrix:
    for num in row:
        flat_list.append(num)

print("Сгенерированная матрица:", matrix)
print("Сумма элементов:", sum(flat_list))