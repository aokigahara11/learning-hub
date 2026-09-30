# Запрашивайте у пользователя вводить число user_number до тех пор, пока оно не будет меньше my_number.
my_number = 10

while True:
    user_number = int(input(f"Введите число меньше {my_number}: "))
    
    if user_number < my_number:
        print(f"Вы ввели число меньше {my_number}: {user_number}")
        break
    else:
        print(f"Число должно быть меньше {my_number}. Попробуйте снова.")