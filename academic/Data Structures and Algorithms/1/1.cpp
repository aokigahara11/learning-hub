#include <iostream>
#include <fstream>
#include <string>
#include <cstdint>
#include <vector>

// Создать запись Студент следующей структуры: ФИО, Дата_рождения – строки, курс, группа- байтовые числа. 
// Написать программу, реализующую следующее меню: 
// добавить элемент в файл
// удалить элемент из файла
// принадлежность элемента файлу
// вывод всех записей на экран

struct Student
{
    std::string fio;
    std::string date_birth;
    uint8_t course;
    uint8_t group;
};

class Students {
public:
    // Формат хранения данных структуры в файле:
    // Иванов Иван Иванович - ФИО
    // 01.01.2000 - Дата рождения
    // 2 122 - Курс, Группа

    std::string file_path;
    Students(std::string path = "students.txt") : file_path(path) {}

    // Добавить студента
    bool add_student(const Student& s) {
        std::ofstream out(file_path, std::ios::app);
        
        if (!out.is_open()) {
            return false;
        }

        out << s.fio << "\n" 
            << s.date_birth << "\n" 
            << static_cast<int>(s.course) << " " 
            << static_cast<int>(s.group) << "\n";
            
        return true;
    }

    // Проверить принадлежность студента файлу
    bool check_student(const std::string& target_fio) const {
        std::ifstream in(file_path);
        
        if (!in.is_open()) {
            return false;
        }

        std::string fio, date_birth;
        int c, g;

        // Цикл считывает первую строку - ФИО, вторую - Дата рождения, после на третей строке
        // переменные c - курс и g - группа
        while (std::getline(in, fio) && std::getline(in, date_birth) && (in >> c >> g)) {
            in.ignore();
            if (fio == target_fio) {
                return true;
            }
        }
        return false;
    }

    // Удалить студента из файла
    bool delete_student(const std::string& target_fio) {
        std::ifstream in(file_path);
        
        if (!in.is_open()) {
            return false;
        }

        // Вектор служит временным хранилищем для будущей перезаписи файла
        std::vector<Student> students;

        Student s;
        int c, g;
        bool found = false;

        // Цикл считывает первую строку - ФИО, вторую - Дата рождения, после на третей строке
        // переменные c - курс и g - группа
        while (std::getline(in, s.fio) && std::getline(in, s.date_birth) && (in >> c >> g)) {
            in.ignore();
            s.course = static_cast<uint8_t>(c);
            s.group = static_cast<uint8_t>(g);

            if (s.fio == target_fio) {
                found = true;
            } else {
                students.push_back(s);
            }
        }
        in.close();

        if (!found) {
            return false;
        }

        // Перезапись файла после успешного удаления
        std::ofstream out(file_path, std::ios::trunc);
        for (const auto& st : students) {
            out << st.fio << "\n" 
                << st.date_birth << "\n" 
                << static_cast<int>(st.course) << " " 
                << static_cast<int>(st.group) << "\n";
        }

        return true;
    }

    // Вывод всех записей на экран
    void print_records() const {
        std::ifstream in(file_path);
        if (!in.is_open()) {
            std::cout << "Файл пуст или еще не создан.\n";
            return;
        }

        Student s;
        int c, g;

        // Цикл считывает первую строку - ФИО, вторую - Дата рождения, после на третей строке
        // переменные c - курс и g - группа
        while (std::getline(in, s.fio) && std::getline(in, s.date_birth) && (in >> c >> g)) {
            in.ignore();
            s.course = static_cast<uint8_t>(c);
            s.group = static_cast<uint8_t>(g);

            std::cout << "ФИО: " << s.fio << "\n"
                      << "Дата рождения: " << s.date_birth << "\n"
                      << "Курс: " << static_cast<int>(s.course) << " "
                      << "Группа: " << static_cast<int>(s.group) << "\n"
                      << "-----------------------------------\n";
        }
    }
};

int main() {
    setlocale(LC_ALL, "Russian");

    Students manager("students.txt");
    int choice = -1;

    while (true) {
        std::cout << "\n--- Главное меню ---\n"
                  << "1. Добавить элемент в файл\n"
                  << "2. Удалить элемент из файла\n"
                  << "3. Проверить принадлежность элемента файлу\n"
                  << "4. Вывод всех записей на экран\n"
                  << "0. Выход\n"
                  << "Выберите действие: ";

        std::cin >> choice;
        std::cin.ignore();

        switch (choice) {
            case 1: {
                Student s;
                int c, g;

                std::cout << "Введите ФИО: ";
                std::getline(std::cin, s.fio);
                std::cout << "Введите дату рождения: ";
                std::getline(std::cin, s.date_birth);
                std::cout << "Введите курс: ";
                std::cin >> c;
                std::cout << "Введите группу: ";
                std::cin >> g;
                std::cin.ignore();

                s.course = static_cast<uint8_t>(c);
                s.group = static_cast<uint8_t>(g);

                if (manager.add_student(s))
                    std::cout << "Студент успешно добавлен!\n";
                else
                    std::cout << "Ошибка при работе с файлом!\n";
                
                break;
            }
            case 2: {
                std::string name;
                std::cout << "Введите ФИО для удаления: ";
                std::getline(std::cin, name);

                if (manager.delete_student(name)) 
                    std::cout << "Запись успешно удалена!\n";
                else
                    std::cout << "Студент не найден или произошла ошибка!\n";

                break;
            }
            case 3: {
                std::string name;
                std::cout << "Введите ФИО для проверки: ";
                std::getline(std::cin, name);

                if (manager.check_student(name))
                    std::cout << "Запись принадлежит файлу!\n";
                else
                    std::cout << "Запись не найдена в файле.\n";

                break;
            }
            case 4: {
                manager.print_records();
                break;
            }
            case 0:
                std::cout << "Завершение работы программы.\n";
                return 0;

            default:
                std::cout << "Некорректный ввод, попробуйте снова!\n";
                break;
        }
    }

    return 0;
}