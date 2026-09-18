#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <windows.h>

// Создать динамический массив вещественных чисел

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    int count = 10;

    std::vector<float> array(count);
    
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    for (int i = 0; i < count; i++) {
        array[i] = static_cast<float>(rand() % 10000) / 100.0f;
    }

    std::cout << "Элементы массива:\n";
    for (float num : array) {
        std::cout << num << " ";
    }
    std::cout << "\n";

    return 0;
}