# Выяснить, сколько нечетных цифр в числе

def option_1(n: int) -> int:
    count = 0

    for digit in str(abs(n)):
        if int(digit) % 2 != 0:
            count += 1

    return count

def option_2(n: int) -> int:
    n = abs(n)
    count = 0
    
    while n > 0:
        digit = n % 10
        if digit % 2 != 0:
            count += 1
        n = n // 10
        
    return count

number = int(input("Введите число: "))
print(f"Количество нечетных цифр в числе: {option_2(number)}")