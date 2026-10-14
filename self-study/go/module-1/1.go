package main

import (
	"fmt"
)

/* Переменные и типы:

Объяви переменную itemName (название товара, тип string).

Объяви переменную itemPrice (цена за единицу товара, тип float64).

Объяви переменную quantity (количество, тип int).

Объяви константу taxRate (налог на продажу, например, 0.13 — 13%) с использованием const.

Строгая типизация (Нюанс №1):

Посчитай общую стоимость без налога (priceWithoutTax = itemPrice * float64(quantity)). Обрати внимание на явное приведение типов, так как quantity — это int, а itemPrice — float64.

Правила компиляции (Нюанс №2):

Все объявленные переменные должны быть использованы в программе (иначе Go не скомпилирует код).

Вывод результата:

Выведи в консоль информацию о товаре, общую сумму без налога, сумму налога и итоговую сумму с учетом налога с помощью fmt.Println или fmt.Printf.

*/

import (
	"fmt"
)

func main() {
	var itemName string = "Ноутбук"
	var itemPrice float64 = 50000.0
	var quantity int = 2
	
	const taxRate = 0.13

	priceWithoutTax := itemPrice * float64(quantity)
	taxAmount := priceWithoutTax * taxRate
	priceWithTax := priceWithoutTax + taxAmount

	fmt.Printf(`
 		Информация о товаре:
 		Название: %s
 		Цена за шт: %.2f
 		Количество: %d
 		Налог (%%): %.0f%%
	`, itemName, itemPrice, quantity, taxRate * 100)

	fmt.Println("Общая цена без налога:", priceWithoutTax)
	fmt.Println("Сумма налога:", taxAmount)
	fmt.Println("Общая цена с учетом налога:", priceWithTax)
}