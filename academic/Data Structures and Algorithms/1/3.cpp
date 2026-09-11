#include <iostream>

// 3) Создать простую очередь вещественных чисел на основе статического массива. 
// Реализовать методы : Добавить элемент, удалить элемент, длина очереди.

class Queue {
public:
    static const int MAX_SIZE = 100;
    float data[MAX_SIZE];
    int first = 0;
    int next = 0;
    int queue_length = 0;

    // Добавить элемент в конец очереди
    bool add(float num) {
        if (queue_length >= MAX_SIZE) {
            std::cout << "Ошибка! Очередь переполнена.";
            return false;
        }

        data[next] = num;

        // Переход к следующей свободной ячейке с зацикливанием по кругу
        next = (next + 1) % MAX_SIZE;

        queue_length++;
        return true;
    }

    // Удалить элемент из начала очереди
    bool pop() {
        if (queue_length == 0) {
            std::cout << "Ошибка! Очередь пустая.";
            return false;
        }

        // Переход к следующей свободной ячейке с зацикливанием по кругу
        first = (first + 1) % MAX_SIZE;

        queue_length--;
        return true;
    }

    // Длина очереди
    int get_queue_length() {
        return queue_length;
    }

    // Получить первый элемент
    int get_first() {
        return data[first];
    }
};

int main() {
    setlocale(LC_ALL, "Russian");

    Queue q;

    q.add(10.5); // Первый
    q.add(20.3);
    q.add(30.8); // Последний

    std::cout << "Длина очереди: " << q.get_queue_length() << "\n";
    std::cout << "Первый элемент: " << q.get_first() << "\n"; // 10.5

    // Удаляем элемент
    q.pop();

    std::cout << "Длина после pop(): " << q.get_queue_length() << "\n"; // 2
    std::cout << "Новый первый элемент: " << q.get_first() << "\n"; // 20.3
    // Так как при очереди удаляется первый элемент, а следующий становится новым первым

    return 0;
}