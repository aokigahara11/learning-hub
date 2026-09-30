# 1.	Найти max значение из трёх величин, 
# определяемых арифметическими выражениями a = tg(x), b = ctg(x), c = ln(x) при за- данных значениях x.
import math


x = float(input("Введите число: "))

a = math.tan(x)
b = 1 / math.tan(x)
c = math.log(x)

print(f"Ответ: {max(a, b, c)}")