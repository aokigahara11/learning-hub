#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cctype>

// Оценить качество хеш-функций, где Fam – фамилия, первая буква – заглавная.
// Запишите данные в файлы таким образом: если не занят адрес,
// то данные записываются в главный файл header.txt, а при возникновении коллизий
// используются вспомогательные файлы 1.txt, 2.txt, 3.txt, …n.txt, где n – порядковый номер символа в алфавите.

// Хеш-формула: h = ord(Fam[1])

struct Data {
    std::string last_name;
    int hash_code;
};

class Utils {
public:
    std::string file_path = "header.txt";
    const int total_alphabet_letters = 26;

    int get_hash(const std::string& last_name) {
        unsigned char b1 = static_cast<unsigned char>(last_name[0]);
        return static_cast<int>(b1);
    }

    // Определение номера буквы латинского алфавита
    int get_alphabet_number(const std::string& last_name) {
        if (last_name.empty()) return 1;
        unsigned char first_char = std::toupper(static_cast<unsigned char>(last_name[0]));
        
        if (first_char >= 'A' && first_char <= 'Z') {
            return (first_char - 'A') + 1;
        }
        return 1;
    }

    // Проверка записи в header.txt
    bool check(int hash) {
        std::ifstream in(file_path);
        
        if (!in.is_open()) {
            return false;
        }

        std::string last_name;
        int hash_in_file;

        while (in >> last_name >> hash_in_file) {
            if (hash == hash_in_file) {
                in.close();
                return true;
            }
        }
        in.close();
        return false;
    }

    // Добавить запись
    bool add(const std::string& last_name) {
        int hash = get_hash(last_name);

        if (!check(hash)) {
            std::ofstream out(file_path, std::ios::app);
            if (!out.is_open()) {
                return false;
            }

            out << last_name << " " << hash << "\n";
            out.close();
            std::cout << "[Info] Written to header.txt: " << last_name << "\n";
            return true;
        } else {
            int n = get_alphabet_number(last_name);
            std::string col_filename = std::to_string(n) + ".txt";
            std::ofstream out_col(col_filename, std::ios::app);

            if (!out_col.is_open()) {
                return false;
            }

            out_col << last_name << " " << hash << "\n";
            out_col.close();
            std::cout << "[Collision] Written to " << col_filename << ": " << last_name << "\n";
            return true;
        }
    }

    // Вывод всех записей
    void print() {
        std::vector<Data> all_data;

        std::ifstream in_header(file_path);
        if (in_header.is_open()) {
            Data d;
            while (in_header >> d.last_name >> d.hash_code) {
                all_data.push_back(d);
            }
            in_header.close();
        }

        for (int i = 1; i <= total_alphabet_letters; ++i) {
            std::string filename = std::to_string(i) + ".txt";
            std::ifstream in_col(filename);

            if (in_col.is_open()) {
                Data d;
                while (in_col >> d.last_name >> d.hash_code) {
                    all_data.push_back(d);
                }
                in_col.close();
            }
        }

        if (all_data.empty()) {
            std::cout << "\n[Info] No records found!\n";
            return;
        }

        std::sort(all_data.begin(), all_data.end(), [](const Data& a, const Data& b) {
            return a.last_name < b.last_name;
        });

        std::cout << "\n--- Sorted Records ---\n";
        for (const auto& item : all_data) {
            std::cout << item.last_name << " (Hash: " << item.hash_code << ")\n";
        }
        std::cout << "----------------------\n";
    }

    // Получить качество хеш-функции
    void get_quality() {
        int header_count = 0;
        int collision_count = 0;

        std::ifstream in_header(file_path);
        if (in_header.is_open()) {
            std::string name;
            int hash;
            while (in_header >> name >> hash) header_count++;
            in_header.close();
        }

        for (int i = 1; i <= total_alphabet_letters; ++i) {
            std::ifstream in_col(std::to_string(i) + ".txt");
            if (in_col.is_open()) {
                std::string name;
                int hash;
                while (in_col >> name >> hash) collision_count++;
                in_col.close();
            }
        }

        int total = header_count + collision_count;
        if (total == 0) {
            std::cout << "\n[Info] No data to evaluate quality.\n";
            return;
        }

        float collision_rate = (static_cast<float>(collision_count) / total) * 100.0f;

        std::cout << "\nHash Function Quality\n";
        std::cout << "Total records: " << total << "\n";
        std::cout << "Records in header.txt: " << header_count << "\n";
        std::cout << "Total collisions: " << collision_count << "\n";
        std::cout << "Collision rate: " << collision_rate << "%\n";
        std::cout << "-----------------------------\n";
    }
};

int main() {
    Utils utils;
    int choice = 0;
    std::string name;

    utils.add("Abramov");
    utils.add("Antonov");
    utils.add("Afanasiev");
    utils.add("Ivanov");
    utils.add("Ignatiev");
    utils.add("Ilyin");
    utils.add("Isakov");

    while (true) {
        std::cout << "\n1. Add new record\n";
        std::cout << "2. View all records (sorted)\n";
        std::cout << "3. Evaluate hash quality\n";
        std::cout << "4. Exit\n";
        std::cout << "Enter your choice: ";
        
        if (!(std::cin >> choice)) {
            std::cout << "Invalid input. Please enter a number.\n";
            std::cin.clear();
            std::cin.ignore(10000, '\n');
            continue;
        }

        switch (choice) {
            case 1:
                std::cout << "Enter last name to add: ";
                std::cin >> name;
                utils.add(name);
                break;
            case 2:
                utils.print();
                break;
            case 3:
                utils.get_quality();
                break;
            case 4:
                std::cout << "Exiting program...\n";
                return 0;
            default:
                std::cout << "Invalid choice! Please try again.\n";
        }
    }

    return 0;
}