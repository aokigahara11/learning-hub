# 4.	Найти min значение из трёх величин, определяемых 
# арифметическими выражениями a = sin(x), b = cos(x), c = ln(x) при заданных значениях x.
import math

x = float(input("Введите число: "))

a = math.sin(x)
b = math.cos(x)
c = math.log(x)

print(f"Ответ: {min(a, b, c)}")

