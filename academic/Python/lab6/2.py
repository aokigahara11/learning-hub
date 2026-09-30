# Пусть дана строка, состоящая из слов, пробелов и знаков препинания. На основании этой строки создайте новую (и выведите ее на консоль):

my_string = "Ф;И;О;Возраст;Категория;_Иванов;Иван;Иванович;23 года;Студент 3 курса;_Петров;Семен;Игоревич;22 года;Студент 2 курса"

records = my_string.split("_")

print(f"{'ФИО':<25} {'Возраст':<15} {'Категория':<20}")
print("-" * 60)

for record in records[1:]:
    data = record.split(";")
    
    surname, name, patronymic, age, category = data[0], data[1], data[2], data[3], data[4]
    
    FIO = f"{surname} {name} {patronymic}"
    
    print(f"{FIO:<25} {age:<15} {category:<20}")