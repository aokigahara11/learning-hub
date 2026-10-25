package main

import (
	"fmt"
)

/*

Создай структуру User с полями:

Username (string)

Balance (float64)

IsActive (bool)

Напиши метод для этой структуры с указателем (*User) под названием TopUp(amount float64), который увеличивает баланс пользователя на переданную сумму.

Напиши еще один метод (можно по значению) GetInfo(), который выводит информацию о пользователе в консоль.

В функции main():

Создай экземпляр пользователя (например, с балансом 1000.0).

Вызови метод пополнения баланса (TopUp).

Вызови метод вывода информации и убедись, что баланс действительно обновился благодаря указателю.

*/

type User struct {
	Username string
	Balance  float64
	IsActive bool
}

func (user *User) TopUp(amount float64) {
	user.Balance += amount
}

func (user User) GetInfo() {
	fmt.Printf("Пользователь: %s | Баланс: %.2f | Активен: %t\n", user.Username, user.Balance, user.IsActive)
}

func main() {
	users := []User{
		{Username: "aoki", Balance: 1000.0, IsActive: true},
		{Username: "alice", Balance: 500.0, IsActive: true},
		{Username: "bob", Balance: 150.0, IsActive: false},
	}

	users[0].TopUp(500.0)
	users[1].TopUp(300.0)

	for _, user := range users {
		user.GetInfo()
	}
}
