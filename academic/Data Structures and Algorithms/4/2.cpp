#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <windows.h>

// Создать хеш-функцию для хранения записей в файл в сортированном виде.  
// Хеш- функцию связать с кодами первых 2 символов Фамилии. 
// Запись состоит из полей :Фамилия, Имя.

struct Data {
    std::string last_name;
    std::string first_name;
    int hash_code;
};

// Хеш-функция
static int hash(const std::string& last_name) {
    unsigned char char1 = std::toupper(static_cast<unsigned char>(last_name[0]));
    unsigned char char2 = std::toupper(static_cast<unsigned char>(last_name[1]));

    return (static_cast<int>(char1) * 256) + static_cast<int>(char2);
}

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    std::vector<Data> people = {
        {"Сидоров", "Алексей"},
        {"Иванов", "Иван"},
        {"Абрамов", "Павел"},
        {"Игнатьев", "Сергей"},
        {"Антонов", "Денис"}
    };


    for (auto& person : people) {
        person.hash_code = hash(person.last_name);
    }

    std::sort(people.begin(), people.end(), [](const Data& a, const Data& b) {
        if (a.hash_code != b.hash_code) {
            return a.hash_code < b.hash_code;
        }
        return a.last_name < b.last_name;
    });

    std::ofstream out_file("sorted_people.txt");
    if (!out_file.is_open()) {
        std::cerr << "Ошибка при открытии файла для записи!" << std::endl;
        return 1;
    }

    for (const auto& person : people) {
        out_file << person.hash_code << " " 
                 << person.last_name << " " 
                 << person.first_name << "\n";
    }

    out_file.close();
    std::cout << "\nДанные успешно сохранены в файл sorted_people.txt!" << std::endl;

    return 0;
}