#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <algorithm>
#include <cmath>

// Сортировать массив целых чисел карманной сортировкой, быстрой сортировкой. 
// Оценить реальное время на сортировку каждым из методов на текущем компьютере. 
// Количество элементов массива не менее  10000.

const int COUNT_BUCKET = 100;
const int COUNT_NUMBERS = 10000;
const int MAX_NUMBER = 10000;

// Карманная сортировка
void sort_bucket(std::vector<int>& array) {
    std::vector<std::vector<int>> buckets(COUNT_BUCKET);

    // Раскладываем числа по пакетам
    for (int num : array) {
        int bucket_index = (num * COUNT_BUCKET) / (MAX_NUMBER + 1);
        buckets[bucket_index].push_back(num);
    }

    array.clear();

    // Сортируем каждые пакеты и добавляем в единный результат
    for (auto& bucket : buckets) {
        std::sort(bucket.begin(), bucket.end());
        for (int num : bucket) {
            array.push_back(num);
        }
    }
}

// Быстрая сортировка
void sort_quick(std::vector<int>& array, int first, int last) {
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
        sort_quick(array, first, j);
    }

    if (i < last) {
        sort_quick(array, i, last);
    }
}

// Вспомогательная функция для заполнения массива случайными числами
void filling_array(std::vector<int>& array, int count, int max_num) {
    srand(static_cast<unsigned int>(time(nullptr)));

    for (int i = 0; i < count; i++) {
        array[i] = rand() % max_num + 1;
    }

    std::cout << "Количество элементов: " << count << std::endl;
}

int main() {
    setlocale(LC_ALL, "Russian");

    std::vector<int> array(COUNT_NUMBERS);

    // Заполняем массив числами
    filling_array(array, COUNT_NUMBERS, MAX_NUMBER);

    // Карманная сортировка
    std::vector<int> arr_bucket_sorted = array;
    auto startBucket = std::chrono::high_resolution_clock::now();
    sort_bucket(arr_bucket_sorted);
    auto endBucket = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> durationBucket = endBucket - startBucket;
    std::cout << "Bucket Sort занял: " << durationBucket.count() << " мс\n";
    
    // Быстрая сортировка
    std::vector<int> array_quick_sorted = array;
    auto startQuick = std::chrono::high_resolution_clock::now();
    sort_quick(array_quick_sorted, 0, COUNT_NUMBERS - 1);
    auto endQuick = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> durationQuick = endQuick - startQuick;
    std::cout << "Quick Sort занял: " << durationQuick.count() << " мс\n";

    double diff = std::abs(durationQuick.count() - durationBucket.count());

    if (durationBucket.count() > durationQuick.count()) {
        std::cout << "Быстрая сортировка быстрее на: " << diff << " мс" << std::endl;
    } else {
        std::cout << "Карманная сортировка быстрее на: " << diff << " мс" << std::endl;
    }

    return 0;
}