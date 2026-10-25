package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"
)

/*

HTTP-сервер должен слушать порт :8080 и обрабатывать запросы по пути /order.

Когда клиент делает запрос на /order:

Сервер мгновенно возвращает клиенту JSON-ответ: {"status": "order accepted", "item": "Laptop"} со статусом 200 OK.

Одновременно с этим (через ключевое слово go)
сервер запускает фоновую горутину, которая имитирует сохранение заказа в PostgreSQL (например, time.Sleep(3 * time.Second)
и вывод в консоль: [PostgreSQL] Заказ успешно сохранен в базу!).

В функции main или внутри обработчика используй sync.WaitGroup, чтобы фоновая горутина корректно отрабатывала и
отчитывалась о завершении в консоли сервера.

*/

// Структура для ответа клиенту
type OrderResponse struct {
	Status string `json:"status"`
	Item   string `json:"item"`
	Code   string `json:"code"`
}

// Фоновая функция, которая имитирует долгую работу с PostgreSQL
func addOrder(wg *sync.WaitGroup) {
	defer wg.Done()

	// Имитируем сохранение в базу данных (3 секунды)
	time.Sleep(3 * time.Second)
	fmt.Println("[PostgreSQL] Заказ успешно сохранен в базу!")
}

func orderHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	response := OrderResponse{
		Status: "order accepted",
		Item:   "Laptop",
		Code:   "200",
	}

	err := json.NewEncoder(w).Encode(response)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var wg sync.WaitGroup
	wg.Add(1)
	go addOrder(&wg)

	wg.Wait()
}

func main() {
	http.HandleFunc("/order", orderHandler)

	fmt.Println("Сервер запущен на http://localhost:8080/order ...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Ошибка при запуске сервера:", err)
	}
}
