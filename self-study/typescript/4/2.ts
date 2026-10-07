// Задание 2: Асинхронный контроллер загрузки данных (AsyncDataLoader)
// Напиши класс AsyncDataLoader<T>:

// Тип состояния:

// type DataState<T> =
//  | { status: "idle" }
//  | { status: "loading" }
//  | { status: "success"; data: T }
//  | { status: "error"; error: string };
// Приватное поле: _state: DataState<T> (начальное значение: { status: "idle" }).

// Геттер: public get state(): DataState<T>, который возвращает текущее состояние.

// Метод execute(requestFn: () => Promise<T>): Promise<void>:

// Переводит _state в положение { status: "loading" }.

// В блоке try вызывает await requestFn().

// При успешном выполнении переводит _state в { status: "success", data }.

// В блоке catch переводит _state в { status: "error", error: error.message } (обработав проверку error instanceof Error).

type DataState<T> =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; error: string };

class AsyncDataLoader<T> {
    private _state: DataState<T> = { status: "idle" };

    public get state(): DataState<T> {
        return this._state;
    }

    public async execute(requestFn: () => Promise<T>): Promise<void> {
        this._state = { status: "loading" };

        try {
            const data = await requestFn();
            this._state = { status: "success", data };
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Unidentified error";
            this._state = { status: "error", error: errorMessage };
        }
    }
}