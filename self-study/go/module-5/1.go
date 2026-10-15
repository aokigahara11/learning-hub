package main

import (
    "fmt"
    "net/http"
)

/* 

Создать структуру Product с полями Name (string) и Price (float64).

Написать функцию-обработчик productHandler(w http.ResponseWriter, r *http.Request), которая 
создает товар (например, "Ноутбук", 75000.0) и выводит о нем информацию через fmt.Fprintf(w, ...).

В функции main() зарегистрировать этот обработчик на путь "/product" и запустить сервер на порту :8080.

*/

type Product struct {
	Name string
	Price float64
}

func productHandler(w http.ResponseWriter, r *http.Request) {
	p := Product{Name: "iPhone", Price: 99000.0}
	
	fmt.Fprintf(w, "Товар: %s; Цена: %.2f руб.\n", p.Name, p.Price)
}

func main() {
	// Регистрием путь для нашего хендлера
	http.HandleFunc("/product", productHandler)

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
	}
}

