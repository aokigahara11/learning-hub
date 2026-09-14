#include <iostream>
#include <string>

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
    setlocale(LC_ALL, "Russian");

    SinglyLinkedList users;

    // Добавление элементов
    users.add({"Иванов", "Иван", "Иванович", "10.05.1995"});
    users.add({"Петров", "Петр", "Петрович", "15.08.1988"});
    users.add({"Сидоров", "Алексей", "Сергеевич", "01.01.2000"});

    users.print();

    // Проверка принадлежности
    std::string search_name = "Петров";
    std::cout << "\nПроверка присутствия фамилии \"" << search_name << "\": "
              << (users.check(search_name) ? "Найден" : "Не найден") << "\n";

    // Удаление элемента
    std::string remove_name = "Петров";
    std::cout << "\nУдаление пользователя с фамилией \"" << remove_name << "\"...\n";
    users.remove(remove_name);

    users.print();

    return 0;
}