#include <iostream>
#include <vector>
#include <algorithm>
#include <windows.h>

// Для сортированного массива В(1000) вещественных чисел реализовать методы последовательного и бинарного поиска. 
// Определить количество шагов необходимых для поиска введенного с клавиатуры элементов первым и вторым методом.

const int SIZE = 1000;

// Последовательный поиск
int linear_search(const std::vector<float>& B, float target, int& steps) {
    steps = 0;

    for (int i = 0; i < B.size(); i++ ) {
        steps++;

        if (B[i] == target) {
            return i;
        }
    }
    return -1;
}

// Бинарный поиск
int binary_search(const std::vector<float>& B, float target, int& steps) {
    steps = 0;
    int low = 0;
    int high = B.size() - 1;

    while (low <= high) {
        steps++;
        int mid = low + (high - low) / 2;

        if (B[mid] == target) {
            return mid;
        }
        
        if (B[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    std::vector<float> B(SIZE);
    for (int i = 0; i < SIZE; ++i) {
        B[i] = (i + 1) * 1.5f;
    }

    int linear_steps = 0;
    int binary_steps = 0;

    float target;
    std::cout << "Введите вещественное число для поиска: ";
    std::cin >> target;

    int index_linear = linear_search(B, target, linear_steps);
    int index_binary = binary_search(B, target, binary_steps);

    std::cout << "Последовательный поиск: ";
    if (index_linear != -1)
        std::cout << "Элемент найден по индексу " << index_linear;
    else
        std::cout << "Элемент не найден";
    std::cout << " (Сделано шагов: " << linear_steps << ")\n";

    std::cout << "Бинарный поиск:         ";
    if (index_binary != -1)
        std::cout << "Элемент найден по индексу " << index_binary;
    else
        std::cout << "Элемент не найден";
    std::cout << " (Сделано шагов: " << binary_steps << ")\n";

    return 0;
}
