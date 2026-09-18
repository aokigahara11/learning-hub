#include <iostream>
#include <string>
#include <windows.h>

//  Создать двусвязный список  для хранения  названий городов Ханты-Мансийского автономного округа. 
// Реализовать методы: Добавить узел, удалить узел, просмотр списка слева 
// направо и справа налево, определение принадлежности элемента списку.

struct Node {
    std::string city_name;
    Node* next;
    Node* prev;

    Node(const std::string& name) : city_name(name), next(nullptr), prev(nullptr) {}
};

class DoublyLinkedList {
private:
    Node* head;
    Node* tail;

public:
    DoublyLinkedList() : head(nullptr), tail(nullptr) {}

    ~DoublyLinkedList() {
        while (head != nullptr) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    // Добавить узел
    void add(const std::string& city) {
        Node* new_node = new Node(city);

        if (head == nullptr) {
            head = new_node;
            tail = new_node;
            return;
        }

        tail->next = new_node;
        new_node->prev = tail;
        tail = new_node;
    }

    // Удалить узел
    bool remove(const std::string& city) {
        Node* current = head;

        while (current != nullptr && current->city_name != city) {
            current = current->next;
        }

        if (current == nullptr) return false;

        if (current == head) {
            head = head->next;
            if (head != nullptr) {
                head->prev = nullptr;
            } else {
                tail = nullptr;
            }
        } 
        else if (current == tail) {
            tail = tail->prev;
            tail->next = nullptr;
        } 
        else {
            current->prev->next = current->next;
            current->next->prev = current->prev;
        }

        delete current;
        return true;
    }

    // Просмотр списка (mode = 0: слева направо, mode = 1: справа налево)
    void print(int mode) const {
        if (head == nullptr) {
            std::cout << "Список городов пуст.\n";
            return;
        }

        if (mode == 0) {
            std::cout << "Список городов слева направо: ";
            Node* current = head;

            while (current != nullptr) {
                std::cout << "[" << current->city_name << "]";
                if (current->next != nullptr) std::cout << " <-> ";
                current = current->next;
            }
            std::cout << "\n";
        }

        if (mode == 1) {
            std::cout << "Список городов справа налево: ";
            Node* current = tail;

            while (current != nullptr) {
                std::cout << "[" << current->city_name << "]";
                if (current->prev != nullptr) std::cout << " <-> ";
                current = current->prev;
            }
            std::cout << "\n";
        }
    }

    // Проверить принадлежности элемента списку
    bool check(const std::string& city) const {
        Node* current = head;
        while (current != nullptr) {
            if (current->city_name == city) {
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

    DoublyLinkedList cities;

    cities.add("Ханты-Мансийск");
    cities.add("Сургут");
    cities.add("Нижневартовск");
    cities.add("Нефтеюганск");

    cities.print(0);
    cities.print(1);

    std::string search_city = "Сургут";
    std::cout << "\nПроверка присутствия города \"" << search_city << "\": "
              << (cities.check(search_city) ? "Найден" : "Не найден") << "\n";

    std::string remove_city = "Сургут";
    std::cout << "\nУдаление города \"" << remove_city << "\"...\n";
    cities.remove(remove_city);

    cities.print(0);

    return 0;
}