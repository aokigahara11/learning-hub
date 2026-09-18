#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <windows.h>

// Реализовать методы последовательного и бинарного поиска для массива записей следующей структуры: 
// Фамилия, дата_рождения, адрес. Методы реализовать для поля Фамилия. 

struct User {
    std::string last_name;
    std::string date_birth;
    std::string address;
};

// Последовательный поиск
int linear_search(const std::vector<User>& users, const std::string& target, int& steps) {
    steps = 0;
    
    for (int i = 0; i < users.size(); i++) {
        steps++;
        
        if (users[i].last_name == target) {
            return i;
        }
    }
    return -1;
}

// Бинарный поиск
int binary_search(const std::vector<User>& users, const std::string& target, int& steps) {
    steps = 0;
    int low = 0;
    int high = static_cast<int>(users.size()) - 1;

    while (low <= high) {
        steps++;
        int mid = low + (high - low) / 2;

        if (users[mid].last_name == target) {
            return mid;
        }
        if (users[mid].last_name < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    std::vector<User> users = {
        {"Иванов", "11.11.2006", "Нижневартовск"},
        {"Петров", "17.05.2006", "Москва"},
        {"Сидоров", "14.07.2006", "Стрежевой"},
        {"Алексеев", "29.04.2006", "Нижневартовск"}
    };

    std::sort(users.begin(), users.end(), [](const User& a, const User& b) {
        return a.last_name < b.last_name;
    });

    std::string target = "Петров";
    int steps_lin = 0, steps_bin = 0;

    int idx_lin = linear_search(users, target, steps_lin);
    int idx_bin = binary_search(users, target, steps_bin);

    if (idx_lin == -1 && idx_bin == -1) {
        std::cout << "Элемент не найден";
    } else {
        std::cout << "Результат поиска по фамилии \"" << target << "\":\n";
        std::cout << "Линейный: индекс " << idx_lin << " (шагов: " << steps_lin << ")\n";
        std::cout << "Бинарный: индекс " << idx_bin << " (шагов: " << steps_bin << ")\n";
    }

    return 0;
}