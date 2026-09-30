# 1. Даны действительные числа x,y. Получить: max(x,y), min(x,y).

a, b = map(float, input("Введите два числа: ").split())

max_ = max(a, b)
min_ = min(a, b)

print(f"Минимальное: {min_}; Максимальное: {max_}")
