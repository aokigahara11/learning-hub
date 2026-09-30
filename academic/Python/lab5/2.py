# Выведите построчно все строки размером менее 10 символов

strings = input("Введите строки через запятую: ").split(',')

for s in strings:
    if len(s) < 10:
        print(s)
