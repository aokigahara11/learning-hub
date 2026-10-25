package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

/*

Что нужно сделать:

Внутри функции productHandler добавь искусственную задержку через time.Sleep(3 * time.Second).

Оберни эту задержку в механизм выбора (select) вместе с r.Context().Done(), чтобы сервер умел вовремя прерывать работу, если запрос был отменен.

Попробуй дописать в productHandler следующий блок:

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

	select {
	case <-time.After(3 * time.Second):
		// Если прошло 3 секунды и клиент не ушел, то отправляем данные товара
		err := json.NewEncoder(w).Encode(p)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	case <-r.Context().Done():
		fmt.Println("Запрос был отменен клиентом")
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
