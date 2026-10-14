package main

import (
	"fmt"
)
/*

Напиши функцию analyzeExpenses(expenses []int) (int, int, float64):

На вход она принимает срез целых чисел ([]int — список трат за несколько дней).

Должна возвращать три значения:

Общую сумму трат (сумма всех элементов среза).

Максимальную трату в списке.

Среднюю трату (float64).

В функции main():

Создай срез трат, например: []int{1200, 450, 3200, 890, 150}.

Вызови свою функцию analyzeExpenses, передав туда этот срез.

Прими все три результата в переменные и красиво выведи их в консоль через fmt.Println или fmt.Printf.

*/

func analyzeExpenses(expenses []int) (int, int, float64) {
	sum := 0
	maxVal := expenses[0]

	for _, val := range expenses {
		sum += val
		if val > maxVal {
			maxVal = val
		}
	}

	average := float64(sum) / float64(len(expenses))

	return sum, maxVal, average
}

func main() {
	expenses := []int{1200, 450, 3200, 890, 150}

	totalSum, maxExpense, avgExpense := analyzeExpenses(expenses)

	fmt.Printf("Все траты: %v\n", expenses)
	fmt.Printf("Общая сумма: %d руб.\n", totalSum)
	fmt.Printf("Самая большая трата: %d руб.\n", maxExpense)
	fmt.Printf("Средняя трата: %.2f руб.\n", avgExpense)
}