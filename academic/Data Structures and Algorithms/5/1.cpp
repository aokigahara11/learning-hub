#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <windows.h>

// Оценить качество хеш-функций, где Fam –фамилия на русском языке, причем первая буква – заглавная.
// Запишите данные в файлы таким образом: если не занят адрес,
// то данные записываются в главный файл header.txt, а при возникновении коллизий
// используются вспомогательные файлы 1.txt, 2.txt, 3.txt, …n.txt, где n – порядковый номер символа в алфавите.
// Реализовать методы:  добавить, просмотр (вывод в сортированном виде)

// Хеш-формула: h = ord(Fam[1])

struct Data {
    std::string last_name;
    int hash_code;
};

class Utils {
public:
    std::string file_path = "header.txt";

    // Получить хеш
    int get_hash(const std::string& last_name) {
        unsigned char b1 = static_cast<unsigned char>(last_name[0]);
        unsigned char b2 = static_cast<unsigned char>(last_name[1]);

        return (static_cast<int>(b1) << 8) | static_cast<int>(b2);
    }

    // Определение номера буквы алфавита (1..33) для UTF-8
    int get_alphabet_number(const std::string& last_name) {
        unsigned char b1 = static_cast<unsigned char>(last_name[0]);
        unsigned char b2 = static_cast<unsigned char>(last_name[1]);

        if (b1 == 0xD0) {
            if (b2 == 0x81) { 
                return 7; // Буква 'Ё'
            }
            
            if (b2 >= 0x90 && b2 <= 0x95) {
                return (b2 - 0x90) + 1; // 'А'..'Е' (1..6)
            }
            
            if (b2 >= 0x96 && b2 <= 0xAF) {
                return (b2 - 0x96) + 8; // 'Ж'..'Я' (8..33)
            }
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
            if (!out.is_open()) return false;

            out << last_name << " " << hash << "\n";
            out.close();
            std::cout << "Записано в header.txt: " << last_name << "\n";
            return true;
        } else {
            int n = get_alphabet_number(last_name);
            std::string col_filename = std::to_string(n) + ".txt";
            std::ofstream out_col(col_filename, std::ios::app);

            if (!out_col.is_open()) return false;

            out_col << last_name << " " << hash << "\n";
            out_col.close();
            std::cout << "Коллизия! Записано в " << col_filename << ": " << last_name << "\n";
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

        for (int i = 1; i <= 33; ++i) {
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

        std::sort(all_data.begin(), all_data.end(), [](const Data& a, const Data& b) {
            return a.last_name < b.last_name;
        });

        for (const auto& item : all_data) {
            std::cout << item.last_name << " (Хеш: " << item.hash_code << ")\n";
        }
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

        for (int i = 1; i <= 33; ++i) {
            std::ifstream in_col(std::to_string(i) + ".txt");
            if (in_col.is_open()) {
                std::string name;
                int hash;
                while (in_col >> name >> hash) collision_count++;
                in_col.close();
            }
        }

        int total = header_count + collision_count;
        if (total == 0) return;

        float collision_rate = (static_cast<float>(collision_count) / total) * 100.0f;

        std::cout << "Количество всех записей: " << total << std::endl;
        std::cout << "Записей в header.txt: " << header_count << std::endl;
        std::cout << "Количество коллизий: " << collision_count << std::endl;
        std::cout << "Процент коллизий: " << collision_rate << "%\n";
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Utils utils;

    utils.add("Альмухаметов");
    utils.add("Иванов");
    utils.add("Вершинин");
    utils.add("Абрамов");
    utils.add("Игнатьев");

    utils.print();
    utils.get_quality();

    return 0;
}