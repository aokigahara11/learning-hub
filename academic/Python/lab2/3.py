# 3.	Даны действительные числа a, b, c. Проверить выполняется ли неравенство a < b < c.

a, b, c = map(float, input("Введите три числа: ").split())

if a < b < c:
    print(True)
else:
    print(False)