def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        context = file.read()
    return context

def sort_last_name(list: list) -> list:
    """Сортировка списка по фамилии"""
    return sorted(list, key=lambda x: x.split()[-1])

def increase_age(list: list) -> list:
    """Увеличить возраст на 1 год для каждого человека в списке"""
    for i in range(len(list)):
        parts = list[i].split()
        parts[-1] = str(int(parts[-1]) + 1)
        list[i] = ' '.join(parts)
    return list

def write_file(file_path: str, list: list):
    with open(file_path, 'w') as file:
        for item in list:
            file.write(f"{item}\n")