#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <windows.h>
#include <cstdint>

// Для хранения записей в файле используете хеш-функцию  Запись имеет структуру Fio:string[20];  kurs, group: byte
// Для разрешения коллизий используйте вспомогательные файлы, имена которых связаны с адресом, 
// а именно имя файла = str(адрес)+’.dat’. Для избежания  ошибки открытия вспомогательных файлов заведите log-файл, 
// в котором построчно  сохраняются имена файлов. Если получившееся имя вспомогательного файла имеется в log-файле, 
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

    // Получить хеш
    int get_hash(const std::string& fio) {
        int hash = 0;

        for (int i = 0; i < 6; ++i) {
            hash += static_cast<unsigned char>(fio[i]);
        }
    
        return hash;
    }

    // Добавить запись
    bool add(const Data& record) {
        int hash = get_hash(record.fio);
        std::string col_filename = std::to_string(hash) + ".dat";

        if (is_log(col_filename)) {
            // Эквивалент Reset
            std::ofstream out(col_filename, std::ios::app);
            if (!out.is_open()) return false;

            out << record.fio << " " << (int)record.course << " " << (int)record.group << "\n";
            out.close();
            std::cout << "Добавлено в существующий файл коллизий (" << col_filename << "): " << record.fio << "\n";
        } else {
            // Эквивалент Rewrite
            add_to_log(col_filename);

            std::ofstream out(col_filename, std::ios::out);
            if (!out.is_open()) return false;

            out << record.fio << " " << (int)record.course << " " << (int)record.group << "\n";
            out.close();
            std::cout << "Создан новый файл коллизий (" << col_filename << ") для: " << record.fio << "\n";
        }
        return true;
    }

    // Проверка, есть ли в логах файл
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

    // Добававить имя в файла в логи
    void add_to_log(const std::string& filename) {
        std::ofstream out(log_file, std::ios::app);
        if (out.is_open()) {
            out << filename << "\n";
            out.close();
        }
    }

    // Поиск записи в файле хеша
    bool find(const std::string& fio) {
        int hash = get_hash(fio);
        std::string col_filename = std::to_string(hash) + ".dat";

        if (!is_log(col_filename)) {
            std::cout << "Запись не найдена (файла с таким адресом не существует).\n";
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
                std::cout << "Найдено: " << f << " | Курс: " << course << " | Группа: " << group << "\n";
                in.close();
                return true;
            }
        }

        in.close();
        std::cout << "Запись с таким ФИО не найдена в файле адреса.\n";
        return false;
    }


    // Вывод всех записейв
    void print() {
        std::ifstream in_log(log_file);
        if (!in_log.is_open()) {
            std::cout << "База данных пуста.\n";
            return;
        }

        std::string filename;
        while (std::getline(in_log, filename)) {
            std::ifstream in_dat(filename);
            if (in_dat.is_open()) {
                std::string f;
                
                int course, group;
                while (in_dat >> f >> course >> group) {
                    std::cout << "ФИО: " << f << " | Курс: " << course << " | Группа: " << group 
                              << " (Файл: " << filename << ")\n";
                }
                in_dat.close();
            }
        }
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Utils utils;

    Data user1 = {"Иванов", 1, 101};
    Data user2 = {"Игнатьев", 2, 202};
    Data user3 = {"Вершинин", 1, 203};
    Data user4 = {"Абрамов", 1, 101};
    Data user5 = {"Альмухаметов", 2, 203};
    Data user6 = {"Ивашикин", 2, 204};

    utils.add(user1);
    utils.add(user2);
    utils.add(user3);
    utils.add(user4);
    utils.add(user5);
    utils.add(user6);

    utils.find("Альмухаметов");

    utils.print();

    return 0;
}