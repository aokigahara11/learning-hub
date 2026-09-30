# Выведите все нечетные элементы построчно списка.
import random

count = int(input("Введите количество элементов списка: "))
list = []

for i in range(count):
    num = random.randint(1, 100)
    list.append(num)

for n in list:
    if n % 2 != 0:
        print(n)