# 2.	Даны действительные числа x, y, z. Вычислить: max(x + y + z, x · y · z), min2 (x + y + z/2, x · y · z) + 1.

x, y, z = map(float, input("Введите три числа: ").split())
max_ = max(x + y + z, x * y * z)
min_ = (min((x + y + z) / 2, x * y * z)) ** 2 + 1
print(f"Максимальное: {max_}; Минимальное: {min_}")