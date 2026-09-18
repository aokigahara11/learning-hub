#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <ctime>
#include <windows.h>

// Cохранить в файле Num.dat несколько целых чисел больших 100 таким образом, 
// чтобы числа записались в сортированном виде. Для этого считать само число -100 
// первым номером записи в файле. Удалить элементы равные 100. 
// Использовать вспомогательный файл. 

class Utils {
public:
    // Вспомогательная функция для заполнения массива случайными числами
    void filling_array(std::vector<int>& array, int count, int min_num, int max_num) {
        srand(static_cast<unsigned int>(time(nullptr)));

        array.resize(count);

        for (int i = 0; i < count; i++) {
            array[i] = min_num + rand() % (max_num - min_num + 1);
        }

        std::cout << "Количество элементов: " << count << std::endl;
    }

    // Быстрая сортировка
    void sort(std::vector<int>& array, int first, int last) {
        if (first >= last) return;

        int pivot = array[first + (last - first) / 2];

        int i = first;
        int j = last;

        while (i <= j) {
            while (array[i] < pivot) {
                i++;
            }

            while (array[j] > pivot) {
                j--;
            }

            if (i <= j) {
                std::swap(array[i], array[j]);
                i++;
                j--;
            }
        }

        if (first < j) {
            sort(array, first, j);
        }

        if (i < last) {
            sort(array, i, last);
        }
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Utils utils;
    std::vector<int> numbers;

    int count = 15;
    int min_num = 95;
    int max_num = 120;
    
    utils.filling_array(numbers, count, min_num, max_num);

    if (!numbers.empty()) {
        utils.sort(numbers, 0, numbers.size() - 1);
    }

    std::ofstream initial_file("Num.dat", std::ios::binary);
    if (!initial_file.is_open()) {
        std::cerr << "Ошибка открытия Num.dat\n";
        return 1;
    }

    int first_elem = -100;
    initial_file.write(reinterpret_cast<char*>(&first_elem), sizeof(first_elem));

    for (int num : numbers) {
        initial_file.write(reinterpret_cast<char*>(&num), sizeof(num));
    }
    
    initial_file.close();

    std::ifstream src("Num.dat", std::ios::binary);
    std::ofstream dst("Temp.dat", std::ios::binary);

    if (!src.is_open() || !dst.is_open()) {
        std::cerr << "Ошибка при открытии файлов!\n";
        return 1;
    }

    int value;
    while (src.read(reinterpret_cast<char*>(&value), sizeof(value))) {
        if (value != 100) {
            dst.write(reinterpret_cast<char*>(&value), sizeof(value));
        }
    }

    src.close();
    dst.close();

    std::remove("Num.dat");
    std::rename("Temp.dat", "Num.dat");

    std::cout << "Элементы равные 100 успешно удалены.\n\n";

    return 0;
}