#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <ctime>
#include <string>
#include <windows.h>

class Utils {
public:
    void filling_array(std::vector<int>& array, int count, int min_num, int max_num) {
        srand(static_cast<unsigned int>(time(nullptr)));
        array.resize(count);
        for (int i = 0; i < count; i++) {
            array[i] = min_num + rand() % (max_num - min_num + 1);
        }
        std::cout << "Количество сгенерированных элементов: " << count << std::endl;
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    Utils utils;
    std::vector<int> numbers;

    int count = 15;
    int min_num = 100;
    int max_num = 118;
    
    utils.filling_array(numbers, count, min_num, max_num);
    std::sort(numbers.begin(), numbers.end());

    std::ofstream initial_file("Num.dat");
    if (!initial_file.is_open()) {
        std::cerr << "Ошибка открытия Num.dat\n";
        return 1;
    }

    for (int current = min_num; current <= max_num; ++current) {
    bool found = false;
    for (int num : numbers) {
        if (num == current) {
            initial_file << current << "\n";
            found = true;
        }
    }

    if (!found) {
        initial_file << "\n";
    }
}
initial_file.close();

    std::ifstream src("Num.dat");
    std::ofstream main_dst("Num_clean.dat");
    std::ofstream dup_dst("Temp.dat");

    if (!src.is_open() || !main_dst.is_open() || !dup_dst.is_open()) {
        std::cerr << "Ошибка открытия файлов!\n";
        return 1;
    }

    std::string line;
    int prev_value = -999999;

    while (std::getline(src, line)) {
        if (line.empty()) {
            main_dst << "\n";
            continue;
        }

        int value = std::stoi(line);

        if (value == 100) {
            continue; 
        }

        if (value == prev_value) {
            dup_dst << value << "\n";
            main_dst << "\n"; 
        } else {
            main_dst << value << "\n";
            prev_value = value;
        }
    }

    src.close();
    main_dst.close();
    dup_dst.close();

    std::remove("Num.dat");
    std::rename("Num_clean.dat", "Num.dat");

    std::ifstream check_main("Num.dat");
    std::cout << "\nСодержимое Num.dat (с \n на месте пропусков):\n";
    while (std::getline(check_main, line)) {
        if (line.empty()) {
            std::cout << "\n";
        } else {
            std::cout << line << "\n";
        }
    }
    check_main.close();

    std::ifstream check_dup("Temp.dat");
    std::cout << "\nСодержимое Temp.dat (повторяющиеся числа):\n";
    while (std::getline(check_dup, line)) {
        std::cout << line << "\n";
    }
    check_dup.close();

    return 0;
}