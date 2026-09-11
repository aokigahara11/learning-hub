#include <iostream>

//  2) Создать стек  вещественных чисел на основе статического массива. 
// Реализовать методы : Добавить элемент, удалить элемент, вершина стека.

class Stack {
public:
    static const int MAX_SIZE = 100;
    float data[MAX_SIZE];
    int top_index = -1;
    
    // Добавить элемент в конец стека
    bool add(float num) {
        if (top_index >= MAX_SIZE - 1) {
            return false;
        }

        data[++top_index] = num;
        return true;
    }

    // Удалить конечный элемент стека
    bool pop() {
        if (top_index < 0) {
            return false;
        }

        top_index--;
        return true;
    }
    
    // Получить вершину стека, то есть последний элемент массива
    float get_top() const {
        if (top_index < 0) {
            return 0.0;
        }

        return data[top_index];
    }
};

int main() {
    Stack stack;

    stack.add(3.14);
    stack.add(10.94);
    stack.add(7.24);

    std::cout << stack.get_top() << "\n";
    return 0;
}