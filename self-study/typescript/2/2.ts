// Задание 2: Делегирование событий (Event Delegation)
// Представь динамический список задач <ul id="todo-list"></ul>, в который кнопки удаления добавляются динамически.

// Требования:

// Найди список #todo-list типа HTMLUListElement.

// На повешенный на <ul> единственный обработчик события click реализуй паттерн делегирования:

// Получи event.target.

// Проверь через target instanceof HTMLElement, кликнул ли пользователь по кнопке с классом .delete-btn (можно использовать метод target.closest('.delete-btn')).

// Если клик был по кнопке удаления, найди родительский элемент списка <li> и удали его из DOM методом .remove().

function initTodoList(): void {
    const todoList = document.querySelector<HTMLUListElement>('#todo-list');
    const deleteBtnClass = '.delete-btn';

    if (!todoList) {
        throw new Error('Не удалось найти элемент списка задач. Проверьте правильность селектора.');
    }

    todoList.addEventListener('click', (event: MouseEvent) => {
        const target = event.target;

        if (target instanceof HTMLElement) {
            const deleteBtn = target.closest(deleteBtnClass);
            
            if (deleteBtn) {
                const listItem = deleteBtn.closest('li');
                if (listItem) {
                    listItem.remove();
                }
            }
        }
    });
}