# кол-во цифр в числе n (см. пример с нахождением суммы цифр числа).

def option_1(n: int) -> int:
    return len(str(abs(n)))

def option_2(n: int) -> int:    
    count = 0
    while n > 0:
        count += 1
        n = n // 10
        
    return count

number = int(input("Введите число: "))
print(f"Количество цифр в числе: {option_2(number)}")

