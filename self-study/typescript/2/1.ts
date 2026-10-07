// Задание 1: Безопасная работа с DOM и формами
// Представь разметку формы входа:

// <input id="email-input" type="email">

// <button id="submit-btn">Войти</button>

// <p id="status-message"></p>

// Требования:

// Напиши функцию initForm(): void.

// Найди все три элемента с помощью document.querySelector<T>().

// Реализуй проверку: если хотя бы один элемент равен null, выбрось понятную ошибку throw new Error(...).

// Повесь обработчик клика на кнопку:

// Считай значение из input.

// Если email пустой, выведи в параграф текст "Заполните email!" и добавь параграфу CSS-класс error (classList.add).

// Если email заполнен, выведи "Успешный вход: <email>", убери класс error и очисти значение инпута.

function initForm(): void {
    // document.querySelector<T>() позволяет указать тип элемента, который мы ожидаем получить
    const emailInput = document.querySelector<HTMLInputElement>('#email-input');
    const submitBtn = document.querySelector<HTMLButtonElement>('#submit-btn');
    const statusMessage = document.querySelector<HTMLParagraphElement>('#status-message');

    if (!emailInput || !submitBtn || !statusMessage) {
        throw new Error('Не удалось найти один или несколько элементов формы. Проверьте правильность селекторов.');
    }

    submitBtn.addEventListener('click', (event: MouseEvent) => {
        const email = emailInput.value.trim(); // используем trim() для удаления пробелов в начале и конце строки

        if (email === '') {
            statusMessage.textContent = 'Заполните email!';
            statusMessage.classList.add('error');
        } else {
            statusMessage.textContent = `Успешный вход: ${email}`;
            statusMessage.classList.remove('error');
            emailInput.value = '';
        }
    });
}

