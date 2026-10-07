// Задание 1: Реактивный Store (State Management)
// Напиши класс Store<T extends object>, который управляет состоянием приложения:

// Конструктор: Принимает начальный объект состояния initialState: T.

// Поля: Приватный массив функций-подписчиков listeners: Array<(state: T) => void> = [] и приватный state: T.

// Метод getState(): Readonly<T>: Возвращает текущее состояние с защитой от случайной мутации (Readonly).

// Метод subscribe(listener: (state: T) => void): () => void:

// Добавляет функцию-подписчика в массив.

// Возвращает функцию отписки (которая при вызове фильтрует/удаляет этот listener из массива).

// Метод update(patch: Partial<T>): void:

// Обновляет состояние через иммутабельное слияние (this.state = { ...this.state, ...patch }).

// Оповещает всех подписчиков, вызывая каждый listener с новым this.state.

class Store<T extends object> {
    private state: T;
    private listeners: Array<(state: T) => void> = [];

    constructor(initialState: T) {
        this.state = initialState;
    }

    getState(): Readonly<T> {
        return this.state;
    }

    subscribe(listener: (state: T) => void): () => void {
        this.listeners.push(listener);
        return () => this.unsubscribe(listener);
    }

    unsubscribe(listener: (state: T) => void): void {
        this.listeners = this.listeners.filter(l => l !== listener);
    }

    update(patch: Partial<T>): void {
        this.state = { ...this.state, ...patch };
        this.notify();
    }

    private notify(): void {
        for (const listener of this.listeners) { // оповещаем всех подписчиков через цикл for...of, чтобы избежать проблем с изменением массива во время итерации
            listener(this.state); // вызываем каждого подписчика с новым состоянием
        }
    }

}