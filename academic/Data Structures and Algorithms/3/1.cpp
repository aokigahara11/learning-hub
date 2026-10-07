#include <iostream>
#include <string>
#include <windows.h>

// Создать односвязный список  для хранения Фамилии, Имени, Отчества в отдельных полях. 
// Реализовать методы: Добавить узел, удалить узел, 
// просмотр списка, определение принадлежности элемента списку.

struct Data {
    std::string last_name;
    std::string name;
    std::string patronymic;
    std::string date_birth;
};

struct Node {
    Data data;
    Node* next;

    Node(const Data& d) : data(d), next(nullptr) {}
};

class SinglyLinkedList {
private:
    Node* head;

public:
    SinglyLinkedList() : head(nullptr) {}

    ~SinglyLinkedList() {
        while (head != nullptr) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    // Добавить узел
    void add(const Data& data) {
        Node* new_node = new Node(data);

        if (head == nullptr) {
            head = new_node;
            return;
        }

        Node* current = head;
        while (current->next != nullptr) {
            current = current->next;
        }

        current->next = new_node;
    }

    // Удалить узел по фамилии
    bool remove(const std::string& last_name) {
        if (head == nullptr) return false;

        // Если нужно удалить самый первый узел
        if (head->data.last_name == last_name) {
            Node* temp = head;
            head = head->next;
            delete temp;
            return true;
        }

        // Ищем элемент перед удаляемым
        Node* current = head;
        while (current->next != nullptr && current->next->data.last_name != last_name) {
            current = current->next;
        }

        if (current->next == nullptr) return false;

        Node* node_to_delete = current->next;
        current->next = node_to_delete->next;
        delete node_to_delete;

        return true;
    }

    // Просмотр списка
    void print() const {
        if (head == nullptr) {
            std::cout << "Список пуст.\n";
            return;
        }

        Node* current = head;
        int index = 1;

        while (current != nullptr) {
            std::cout << index++ << ". " 
                      << current->data.last_name << " "
                      << current->data.name << " "
                      << current->data.patronymic << " | Дата рождения: "
                      << current->data.date_birth << "\n";
            current = current->next;
        }
    }

    // Определение принадлежности элемента списку
    bool check(const std::string& last_name) const {
        Node* current = head;

        while (current != nullptr) {
            if (current->data.last_name == last_name) {
                return true;
            }
            current = current->next;
        }

        return false;
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    SinglyLinkedList users;
    int choice = 0;

    users.add({"Иванов", "Иван", "Иванович", "10.05.1995"});
    users.add({"Петров", "Петр", "Петрович", "15.08.1988"});
    users.add({"Сидоров", "Алексей", "Сергеевич", "01.01.2000"});

    while (true) {
        std::cout << "1. Добавить запись\n";
        std::cout << "2. Удалить запись по фамилии\n";
        std::cout << "3. Просмотреть список\n";
        std::cout << "4. Проверить наличие по фамилии\n";
        std::cout << "0. Выход\n";
        std::cout << "Выберите действие: ";
        std::cin >> choice;

        switch (choice) {
            case 1: {
                Data data;
                std::cout << "Введите фамилию: ";
                std::cin >> data.last_name;
                std::cout << "Введите имя: ";
                std::cin >> data.name;
                std::cout << "Введите отчество: ";
                std::cin >> data.patronymic;
                std::cout << "Введите дату рождения: ";
                std::cin >> data.date_birth;

                users.add(data);
                std::cout << "Запись успешно добавлена!\n";
                break;
            }
            case 2: {
                std::string last_name;
                std::cout << "Введите фамилию для удаления: ";
                std::cin >> last_name;

                if (users.remove(last_name)) {
                    std::cout << "Запись с фамилией \"" << last_name << "\" успешно удалена.\n";
                } else {
                    std::cout << "Запись с фамилией \"" << last_name << "\" не найдена.\n";
                }
                break;
            }
            case 3:
                std::cout << "\n--- Список пользователей ---\n";
                users.print();
                break;

            case 4: {
                std::string last_name;
                std::cout << "Введите фамилию для поиска: ";
                std::cin >> last_name;

                if (users.check(last_name)) {
                    std::cout << "Пользователь с фамилией \"" << last_name << "\" присутствует в списке.\n";
                } else {
                    std::cout << "Пользователь с фамилией \"" << last_name << "\" не найден.\n";
                }
                break;
            }
            case 0:
                std::cout << "Завершение работы программы.\n";
                return 0;

            default:
                std::cout << "Неверный выбор! Попробуйте снова.\n";
                break;
        }
    }

    return 0;
}