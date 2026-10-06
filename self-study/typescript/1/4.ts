// Задание 4: Реализация исчерпывающей проверки (Exhaustive Check с типом never)
// Создай enum UIState { Loading, Success, Error, Empty }.

// Напиши функцию renderState(state: UIState): string, которая использует конструкцию switch (state).

// В секции default напиши код с проверкой типа never, который на этапе компиляции вызовет ошибку, 
// если кто-то добавит новое состояние в UIState, но забудет обработать его в switch.

enum UIState {
    Loading,
    Success,
    Error,
    Empty
}

function renderState(state: UIState): string {
    switch (state) {
        case UIState.Loading:
            return "Загрузка...";
        case UIState.Success:
            return "Успех!";
        case UIState.Error:
            return "Ошибка!";
        case UIState.Empty:
            return "Пусто!";
        default:
            const _exhaustiveCheck: never = state;
            throw new Error(`Неизвестное состояние: ${_exhaustiveCheck}`);
    }
}