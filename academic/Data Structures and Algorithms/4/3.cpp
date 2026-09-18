#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <windows.h>

// Создать множество для хранения названий городов на основе 2 –направленного связного списка.
// Реализовать операторы : Добавить элемент, удалить элемент, мощность множества, 
// просмотр всех элементов, принадлежность элемента множеству.

class Set {
public:
    struct Node {
        std::string city;
        Node* next;
        Node* prev;

        Node(const std::string& name) : city(name), next(nullptr), prev(nullptr) {}
    };

    Node* head;
    Node* tail;
    size_t element_count;

    Set() : head(nullptr), tail(nullptr), element_count(0) {}

    ~Set() {
        Node* current = head;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }

    // Принадлежность элемента множеству
    bool check(const std::string& city) const {
        Node* current = head;

        while (current != nullptr) {
            if (current->city == city) {
                return true;
            }
            current = current->next;
        }
        return false;
    }

    // Добавить элемент
    bool add(const std::string& city) {
        if (check(city)) {
            return false;
        }

        Node* new_node = new Node(city);

        if (head == nullptr) {
            head = new_node;
            tail = new_node;
        } else {
            tail->next = new_node;
            new_node->prev = tail;
            tail = new_node;
        }

        element_count++;
        return true;
    }

    // Удалить элемент
    bool remove(const std::string& city) {
        Node* current = head;

        while (current != nullptr && current->city != city) {
            current = current->next;
        }

        if (current == nullptr) {
            return false;
        }

        if (current == head) {
            head = head->next;
            if (head != nullptr) {
                head->prev = nullptr;
            } else {
                tail = nullptr;
            }
        } else if (current == tail) {
            tail = tail->prev;
            tail->next = nullptr;
        } else {
            current->prev->next = current->next;
            current->next->prev = current->prev;
        }

        delete current;
        element_count--;
        return true;
    }

    // Мощность множества
    size_t get_power() const {
        return element_count;
    }

    // Просмотр всех элементов
    void print() const {
        if (head == nullptr) {
            std::cout << "Список городов пуст.\n";
            return;
        }

        std::cout << "Список городов: ";
        Node* current = head;

        while (current != nullptr) {
            std::cout << "[" << current->city << "]";
            if (current->next != nullptr) std::cout << " <-> ";
            current = current->next;
        }
        std::cout << "\n";
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Set city_set;

    city_set.add("Москва");
    city_set.add("Сургут");
    city_set.add("Тюмень");
    
    city_set.print();
    std::cout << "Мощность множества: " << city_set.get_power() << "\n\n";

    std::cout << "Принадлежит ли " << "Москва" << " множеству? ";

    if (city_set.check("Москва")) {
        std::cout << "Да\n\n";
    } else {
        std::cout << "Нет\n\n";
    }

    std::cout << "Удаление города Москва..." << std::endl;
    city_set.remove("Москва");

    city_set.print();
    std::cout << "Новая мощность множества: " << city_set.get_power() << std::endl;

    return 0;
}