# 6. Вывести на экран числовой ряд действительных чисел от n до m с шагом 0,2.

n, m = map(int, input("Введите два числа: ").split())

current = n
while current <= m:
    print(round(current, 2))
    current += 0.2