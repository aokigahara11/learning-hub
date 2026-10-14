#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdint>

// Для хранения записей в файле используете хеш-функцию. Запись имеет структуру Fio: string[20]; kurs, group: byte
// Для разрешения коллизий используйте вспомогательные файлы, имена которых связаны с адресом, 
// а именно имя файла = str(адрес)+’.dat’. Для избежания ошибки открытия вспомогательных файлов заведите log-файл, 
// в котором построчно сохраняются имена файлов. Если получившееся имя вспомогательного файла имеется в log-файле, 
// то применяется процедура Reset(t), в противном случае – Rewrite(t).
// Реализуйте операторы: добавить запись, поиск записи, просмотр всех значений.

// Хеш-формула: h = ord(Fam[1]) + ord(Fam[2]) + ord(Fam[3])

struct Data
{
    std::string fio;
    uint8_t course;
    uint8_t group;
};

class Utils {
public:
    std::string log_file = "log.txt";

    // Получить хеш на основе первых символов строки (по формуле суммы кодов первых символов)
    int get_hash(const std::string& fio) {
        int hash = 0;

        for (int i = 0; i < 3 && i < fio.length(); ++i) {
            hash += static_cast<unsigned char>(fio[i]);
        }
    
        return hash;
    }

    // Добавить запись
    bool add(const Data& record) {
        int hash = get_hash(record.fio);
        std::string col_filename = std::to_string(hash) + ".dat";

        if (is_log(col_filename)) {
            // Эквивалент Reset (добавление в конец существующего файла)
            std::ofstream out(col_filename, std::ios::app);
            if (!out.is_open()) return false;

            out << record.fio << " " << (int)record.course << " " << (int)record.group << "\n";
            out.close();
            std::cout << "[Collision] Added to existing file (" << col_filename << "): " << record.fio << "\n";
        } else {
            // Эквивалент Rewrite (создание нового файла и запись в лог)
            add_to_log(col_filename);

            std::ofstream out(col_filename, std::ios::out);
            if (!out.is_open()) return false;

            out << record.fio << " " << (int)record.course << " " << (int)record.group << "\n";
            out.close();
            std::cout << "[New File] Created new collision file (" << col_filename << ") for: " << record.fio << "\n";
        }
        return true;
    }

    // Проверка, есть ли имя файла в log-файле
    bool is_log(const std::string& filename) {
        std::ifstream in(log_file);
        if (!in.is_open()) return false;

        std::string line;
        while (std::getline(in, line)) {
            if (line == filename) {
                in.close();
                return true;
            }
        }
        in.close();
        return false;
    }

    // Добавить имя файла в лог
    void add_to_log(const std::string& filename) {
        std::ofstream out(log_file, std::ios::app);
        if (out.is_open()) {
            out << filename << "\n";
            out.close();
        }
    }

    // Поиск записи в файле по хеш-адресу
    bool find(const std::string& fio) {
        int hash = get_hash(fio);
        std::string col_filename = std::to_string(hash) + ".dat";

        if (!is_log(col_filename)) {
            std::cout << "[Search] Record not found (no file exists for this address).\n";
            return false;
        }

        std::ifstream in(col_filename);
        if (!in.is_open()) { 
            return false;
        }

        std::string f;
        int course, group;

        while (in >> f >> course >> group) {
            if (f == fio) {
                std::cout << "[Found] Name: " << f << " | Course: " << course << " | Group: " << group << "\n";
                in.close();
                return true;
            }
        }

        in.close();
        std::cout << "[Search] Record with this name was not found in the address file.\n";
        return false;
    }

    // Вывод всех записей из всех файлов, зафиксированных в логе
    void print() {
        std::ifstream in_log(log_file);
        if (!in_log.is_open()) {
            std::cout << "[Info] Database is empty (log file not found).\n";
            return;
        }

        std::string filename;
        std::cout << "\n--- All Records in Database ---\n";
        while (std::getline(in_log, filename)) {
            std::ifstream in_dat(filename);
            if (in_dat.is_open()) {
                std::string f;
                int course, group;
                while (in_dat >> f >> course >> group) {
                    std::cout << "Name: " << f << " | Course: " << (int)course 
                              << " | Group: " << (int)group << " (File: " << filename << ")\n";
                }
                in_dat.close();
            }
        }
        std::cout << "-------------------------------\n";
    }
};

int main() {
    Utils utils;
    int choice = 0;
    std::string name;
    int course, group;

    while (true) {
        std::cout << "1. Add new record\n";
        std::cout << "2. Search record\n";
        std::cout << "3. View all records\n";
        std::cout << "4. Exit\n";
        std::cout << "Enter your choice: ";

        if (!(std::cin >> choice)) {
            std::cout << "Invalid input. Please enter a number.\n";
            std::cin.clear();
            std::cin.ignore(10000, '\n');
            continue;
        }

        switch (choice) {
            case 1: {
                Data new_record;
                std::cout << "Enter Last Name (FIO): ";
                std::cin >> new_record.fio;
                std::cout << "Enter Course (1-4): ";
                int c;
                std::cin >> c;
                new_record.course = static_cast<uint8_t>(c);
                std::cout << "Enter Group: ";
                int g;
                std::cin >> g;
                new_record.group = static_cast<uint8_t>(g);

                utils.add(new_record);
                break;
            }
            case 2:
                std::cout << "Enter Last Name to search: ";
                std::cin >> name;
                utils.find(name);
                break;
            case 3:
                utils.print();
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