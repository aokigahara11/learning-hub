list_students = [
    ['3502', ['Акулова Алена', 'Бабушкина Ксения', 'Иванов Иван']],
    ['БОВ-421102', ['Петров Петр', 'Сидоров Сидор']],
    ['БО-331103', ['Смирнова Анна', 'Кузнецов Алексей']]
]

target_group = input("Введите название группы: ")

for group in list_students:
    group_name = group[0]
    
    if group_name == target_group:
        print(f'{group_name}')
        
        for student in group[1]:
            print(f'\t{student}')
        break
else:
    print(f"Группа {target_group} не найдена.")

