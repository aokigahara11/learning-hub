package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

/*

Пересобрать предыдущий код, но с использованием JSON

*/

type Product struct {
	ID    int     `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

func productHandler(w http.ResponseWriter, r *http.Request) {

	// Передаём клиенту, о том что в ответе лежит JSON
	w.Header().Set("Content-Type", "application/json")

	p := Product{
		ID:    1,
		Name:  "Компьютер",
		Price: 75000.0,
	}

	// Кодируем результат в JSON и отправляем в ResponseWriter
	err := json.NewEncoder(w).Encode(p)

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func main() {
	http.HandleFunc("/product", productHandler)

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
	}
}
